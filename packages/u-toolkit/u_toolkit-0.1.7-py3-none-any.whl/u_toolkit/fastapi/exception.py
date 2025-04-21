from collections.abc import Callable, Sequence
from typing import Generic, Literal, Protocol, cast

from fastapi import Response, status
from fastapi.responses import JSONResponse, ORJSONResponse
from fastapi.utils import is_body_allowed_for_status_code
from pydantic import BaseModel, create_model

from u_toolkit.pydantic.type_vars import BaseModelT


try:
    import orjson
except ImportError:  # pragma: nocover
    orjson = None  # type: ignore


class WrapperError(BaseModel, Generic[BaseModelT]):  # type: ignore
    @classmethod
    def create(
        cls: type["WrapperError[BaseModelT]"],
        model: BaseModelT,
    ) -> "WrapperError[BaseModelT]":
        raise NotImplementedError


class EndpointError(WrapperError, Generic[BaseModelT]):
    error: BaseModelT

    @classmethod
    def create(cls, model: BaseModelT):
        return cls(error=model)


class HTTPErrorInterface(Protocol):
    status: int

    @classmethod
    def response_class(cls) -> type[BaseModel]: ...


class NamedHTTPError(Exception, Generic[BaseModelT]):
    status: int = status.HTTP_400_BAD_REQUEST
    code: str | None = None
    targets: Sequence[str] | None = None
    target_transform: Callable[[str], str] | None = None
    message: str | None = None
    wrapper_class: type[WrapperError[BaseModelT]] | None = EndpointError

    @classmethod
    def error_name(cls):
        return cls.__name__.removesuffix("Error")

    @classmethod
    def model_class(cls) -> type[BaseModelT]:
        type_ = cls.error_name()
        error_code = cls.code or type_
        kwargs = {
            "code": (Literal[error_code], ...),
            "message": (Literal[cls.message] if cls.message else str, ...),
        }
        if cls.targets:
            kwargs["target"] = (Literal[*cls.transformed_targets()], ...)

        return cast(type[BaseModelT], create_model(f"{type_}Model", **kwargs))

    @classmethod
    def error_code(cls):
        return cls.code or cls.error_name()

    @classmethod
    def transformed_targets(cls) -> list[str]:
        if cls.targets:
            result = []
            for i in cls.targets:
                if cls.target_transform:
                    result.append(cls.target_transform(i))
                else:
                    result.append(i)
            return result
        return []

    def __init__(
        self,
        *,
        message: str | None = None,
        target: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        kwargs = {
            "code": self.error_code(),
            "message": message or "operation failed",
        }

        if target:
            if self.target_transform:
                target = self.target_transform(target)
            kwargs["target"] = target
            kwargs["message"] = kwargs["message"].format(target=target)

        self.model = self.model_class()(**kwargs)
        self.data: BaseModel = (
            self.wrapper_class.create(self.model)
            if self.wrapper_class is not None
            else self.model
        )

        self.headers = headers

    def __str__(self) -> str:
        return f"{self.status}: {self.data.error.code}"  # type: ignore

    def __repr__(self) -> str:
        return f"{self.model_class: str(self.error)}"

    @classmethod
    def response_class(cls):
        model = cls.model_class()
        return cls.wrapper_class if cls.wrapper_class is not None else model

    @classmethod
    def response_schema(cls):
        return {cls.status: {"model": cls.response_class()}}


def named_http_error_handler(_, exc: NamedHTTPError):
    headers = exc.headers

    if not is_body_allowed_for_status_code(exc.status):
        return Response(status_code=exc.status, headers=headers)

    if orjson:
        return ORJSONResponse(
            exc.data.model_dump(exclude_none=True),
            status_code=exc.status,
            headers=headers,
        )

    return JSONResponse(
        exc.data.model_dump(exclude_none=True),
        status_code=exc.status,
        headers=headers,
    )
