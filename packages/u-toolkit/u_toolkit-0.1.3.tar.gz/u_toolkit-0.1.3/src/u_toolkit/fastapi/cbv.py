import inspect
import re
from collections.abc import Callable
from enum import Enum, StrEnum, auto
from functools import partial, update_wrapper, wraps
from typing import Any, Literal, NamedTuple, Protocol, Self, TypeVar, cast

from fastapi import APIRouter, Depends
from pydantic.alias_generators import to_snake

from u_toolkit.decorators import DefineMethodParams, define_method_handler
from u_toolkit.fastapi.helpers import get_depend_from_annotation, is_depend
from u_toolkit.fastapi.responses import Response, build_responses
from u_toolkit.helpers import is_annotated
from u_toolkit.merge import deep_merge_dict
from u_toolkit.signature import update_parameters, with_parameter


class EndpointsClassInterface(Protocol):
    dependencies: tuple | None = None
    responses: tuple[Response, ...] | None = None
    prefix: str | None = None
    tags: tuple[str | Enum, ...] | None = None
    deprecated: bool | None = None

    @classmethod
    def build_self(cls) -> Self:
        return cls()


_T = TypeVar("_T")
EndpointsClassInterfaceT = TypeVar(
    "EndpointsClassInterfaceT",
    bound=EndpointsClassInterface,
)


LiteralUpperMethods = Literal[
    "GET",
    "POST",
    "PATCH",
    "PUT",
    "DELETE",
    "OPTIONS",
    "HEAD",
    "TRACE",
]
LiteralLowerMethods = Literal[
    "get",
    "post",
    "patch",
    "put",
    "delete",
    "options",
    "head",
    "trace",
]


class Methods(StrEnum):
    GET = auto()
    POST = auto()
    PATCH = auto()
    PUT = auto()
    DELETE = auto()
    OPTIONS = auto()
    HEAD = auto()
    TRACE = auto()


METHOD_PATTERNS = {
    method: re.compile(f"^({method}_|{method})", re.IGNORECASE)
    for method in Methods
}

_FnName = str


class EndpointInfo(NamedTuple):
    fn: Callable
    original_name: str
    method: Methods
    method_pattern: re.Pattern
    path: str


def get_method(name: str):
    for method, method_pattern in METHOD_PATTERNS.items():
        if method_pattern.search(name):
            return method, method_pattern
    return None


def valid_endpoint(name: str):
    if get_method(name) is None:
        raise ValueError("Invalid endpoint function.")


def iter_endpoints(cls: type[_T]):
    prefix = "/"

    if not cls.__name__.startswith("_"):
        prefix += f"{to_snake(cls.__name__)}"

    for name, fn in inspect.getmembers(
        cls,
        lambda arg: inspect.ismethoddescriptor(arg) or inspect.isfunction(arg),
    ):
        paths = [prefix]

        if method := get_method(name):
            path = method[1].sub("", name).replace("__", "/")
            if path:
                paths.append(path)

            yield EndpointInfo(
                fn=fn,
                original_name=name,
                path="/".join(paths),
                method=method[0],
                method_pattern=method[1],
            )


def iter_dependencies(cls: type[_T]):
    _split = re.compile(r"\s+|:|=")
    dependencies: dict = dict(inspect.getmembers(cls, is_depend))
    for name, type_ in inspect.get_annotations(cls).items():
        if is_annotated(type_):
            dependency = get_depend_from_annotation(type_)
            dependencies[name] = dependency

    for line in inspect.getsource(cls).split("\n"):
        token: str = _split.split(line.strip(), 1)[0]
        for name, dep in dependencies.items():
            if name == token:
                yield token, dep


_CBVEndpointParamName = Literal[
    "path",
    "tags",
    "dependencies",
    "responses",
    "response_model",
    "status",
    "deprecated",
    "methods",
]


class CBV:
    def __init__(self, router: APIRouter | None = None) -> None:
        self.router = router or APIRouter()

        self._state: dict[
            type[EndpointsClassInterface],
            dict[_FnName, dict[_CBVEndpointParamName, Any]],
        ] = {}

        self._initialed_state: dict[
            type[EndpointsClassInterface], EndpointsClassInterface
        ] = {}

    def create_route(
        self,
        *,
        cls: type[EndpointsClassInterfaceT],
        path: str,
        method: Methods | LiteralUpperMethods | LiteralLowerMethods,
        method_name: str,
    ):
        class_tags = list(cls.tags) if cls.tags else []
        endpoint_tags: list[str | Enum] = (
            self._state[cls][method_name].get("tags") or []
        )
        tags = class_tags + endpoint_tags

        class_dependencies = list(cls.dependencies) if cls.dependencies else []
        endpoint_dependencies = (
            self._state[cls][method_name].get("dependencies") or []
        )
        dependencies = class_dependencies + endpoint_dependencies

        class_responses = cls.responses or []
        endpoint_responses = (
            self._state[cls][method_name].get("responses") or []
        )
        responses = build_responses(*class_responses, *endpoint_responses)

        status_code = self._state[cls][method_name].get("status")

        deprecated = self._state[cls][method_name].get(
            "deprecated", cls.deprecated
        )

        response_model = self._state[cls][method_name].get("response_model")

        endpoint_methods = self._state[cls][method_name].get("methods") or [
            method
        ]

        path = self._state[cls][method_name].get("path") or path

        return self.router.api_route(
            path,
            methods=endpoint_methods,
            tags=tags,
            dependencies=dependencies,
            response_model=response_model,
            responses=responses,
            status_code=status_code,
            deprecated=deprecated,
        )

    def info(
        self,
        *,
        path: str | None = None,
        methods: list[Methods | LiteralUpperMethods | LiteralLowerMethods]
        | None = None,
        tags: list[str | Enum] | None = None,
        dependencies: list | None = None,
        responses: list[Response] | None = None,
        response_model: Any | None = None,
        status: int | None = None,
        deprecated: bool | None = None,
    ):
        state = self._state
        initial_state = self._initial_state
        data: dict[_CBVEndpointParamName, Any] = {
            "path": path,
            "methods": methods,
            "tags": tags,
            "dependencies": dependencies,
            "responses": responses,
            "response_model": response_model,
            "status": status,
            "deprecated": deprecated,
        }

        def handle(params: DefineMethodParams):
            initial_state(params.method_class)
            deep_merge_dict(
                state,
                {params.method_class: {params.method_name: data}},
            )

        return define_method_handler(handle)

    def _initial_state(self, cls: type[_T]) -> EndpointsClassInterface:
        if result := self._initialed_state.get(cls):  # type: ignore
            return result

        self._update_cls(cls)
        n_cls = cast(type[EndpointsClassInterface], cls)

        default_data = {}
        for endpoint in iter_endpoints(n_cls):
            default_data[endpoint.original_name] = {}

        self._state.setdefault(n_cls, default_data)
        result = self._build_cls(n_cls)
        self._initialed_state[n_cls] = result
        return result

    def _update_cls(self, cls: type[_T]):
        for extra_name in EndpointsClassInterface.__annotations__:
            if not hasattr(cls, extra_name):
                setattr(cls, extra_name, None)

            # TODO: 加个如果存在属性, 校验属性类型是否是预期的

    def _build_cls(self, cls: type[_T]) -> _T:
        if inspect.isfunction(cls.__init__) and hasattr(cls, "build_self"):
            return cast(type[EndpointsClassInterface], cls).build_self()  # type: ignore
        return cls()

    def __create_class_dependencies_injector(
        self, cls: type[EndpointsClassInterfaceT]
    ):
        """将类的依赖添加到函数实例上

        ```python
        @cbv
        class A:
            a = Depends(lambda: id(object()))

            def get(self):
                # 使得每次 self.a 可以访问到当前请求的依赖
                print(self.a)
        ```
        """

        def collect_cls_dependencies(**kwargs):
            return kwargs

        parameters = [
            inspect.Parameter(
                name=name,
                kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                default=dep,
            )
            for name, dep in iter_dependencies(cls)
        ]

        update_parameters(collect_cls_dependencies, *parameters)

        def decorator(method: Callable):
            method_name = method.__name__

            cls_fn = getattr(cls, method_name)
            sign_cls_fn = partial(cls_fn)
            update_wrapper(sign_cls_fn, cls_fn)

            parameters, *_ = with_parameter(
                sign_cls_fn,
                name=collect_cls_dependencies.__name__,
                default=Depends(collect_cls_dependencies),
            )

            update_parameters(sign_cls_fn, *(parameters[1:]))

            @wraps(sign_cls_fn)
            def wrapper(*args, **kwargs):
                instance = self._build_cls(cls)
                dependencies = kwargs.pop(collect_cls_dependencies.__name__)
                for dep_name, dep_value in dependencies.items():
                    setattr(instance, dep_name, dep_value)
                fn = getattr(instance, method_name)
                return fn(*args, **kwargs)

            return wrapper

        return decorator

    def __call__(self, cls: type[_T]) -> type[_T]:
        instance = self._initial_state(cls)
        cls_ = cast(type[EndpointsClassInterface], cls)

        decorator = self.__create_class_dependencies_injector(cls_)

        for endpoint_info in iter_endpoints(cls):
            route = self.create_route(
                cls=cast(type[EndpointsClassInterface], cls),
                path=endpoint_info.path,
                method=endpoint_info.method,
                method_name=endpoint_info.original_name,
            )
            method = getattr(instance, endpoint_info.original_name)
            endpoint = decorator(method)
            route(endpoint)

        return cls
