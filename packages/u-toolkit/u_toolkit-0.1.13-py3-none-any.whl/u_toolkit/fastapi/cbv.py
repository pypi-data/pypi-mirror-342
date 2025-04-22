import inspect
import re
from collections.abc import Callable
from enum import Enum, StrEnum, auto
from functools import partial, update_wrapper, wraps
from typing import (
    Generic,
    Literal,
    NamedTuple,
    NotRequired,
    TypeVar,
    TypedDict,
    cast,
    overload,
)

from fastapi import APIRouter, Depends
from pydantic.alias_generators import to_snake

from u_toolkit.decorators import DefineMethodParams, define_method_handler
from u_toolkit.fastapi.helpers import get_depend_from_annotation, is_depend
from u_toolkit.fastapi.responses import Response, build_responses
from u_toolkit.helpers import is_annotated
from u_toolkit.merge import deep_merge_dict
from u_toolkit.signature import (
    list_parameters,
    update_parameters,
    with_parameter,
)


_T = TypeVar("_T")


LiteralUpperMethod = Literal[
    "GET",
    "POST",
    "PATCH",
    "PUT",
    "DELETE",
    "OPTIONS",
    "HEAD",
    "TRACE",
]
LiteralLowerMethod = Literal[
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


RequestMethod = Methods | LiteralLowerMethod | LiteralUpperMethod


METHOD_PATTERNS = {
    method: re.compile(f"^({method}_|{method})", re.IGNORECASE)
    for method in Methods
}


_FnName = str


_MethodInfo = tuple[RequestMethod, re.Pattern[str]]


def get_method(name: str) -> _MethodInfo | None:
    for method, method_pattern in METHOD_PATTERNS.items():
        if method_pattern.search(name):
            return method, method_pattern
    return None


class EndpointInfo(NamedTuple):
    handle: Callable
    original_handle_name: str
    handle_name: str
    method: RequestMethod
    method_pattern: re.Pattern
    path: str


def iter_endpoints(
    cls: type[_T],
    valid_method: Callable[[str, Callable], list[_MethodInfo] | None]
    | None = None,
):
    prefix = ""

    if not cls.__name__.startswith("_"):
        prefix += f"/{to_snake(cls.__name__)}"

    for name, handle in inspect.getmembers(
        cls,
        lambda arg: inspect.ismethoddescriptor(arg) or inspect.isfunction(arg),
    ):
        paths = [prefix]

        methods: list[_MethodInfo] = []
        from_valid_method = False

        if valid_method:
            if results := valid_method(name, handle):
                methods.extend(results)
            if methods:
                from_valid_method = True

        if not methods and (method := get_method(name)):
            methods.append(method)

        for method, pattern in methods:
            handle_name = name if from_valid_method else pattern.sub("", name)
            path = handle_name.replace("__", "/")
            if path:
                paths.append(path)

            yield EndpointInfo(
                handle=handle,
                original_handle_name=name,
                handle_name=handle_name,
                path="/".join(paths),
                method=method,
                method_pattern=pattern,
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


class CBVRoutesInfo(TypedDict):
    path: NotRequired[str | None]
    tags: NotRequired[list[str | Enum] | None]
    dependencies: NotRequired[list | None]
    responses: NotRequired[list[Response] | None]
    deprecated: NotRequired[bool | None]


class CBVRouteInfo(CBVRoutesInfo, Generic[_T]):
    methods: NotRequired[list[RequestMethod] | None]
    response_model: NotRequired[type[_T] | None]
    status: NotRequired[int | None]


class CBV:
    def __init__(self, router: APIRouter | None = None) -> None:
        self.router = router or APIRouter()

        self._state: dict[type, dict[_FnName, CBVRouteInfo]] = {}
        self._cls_routes_extra: dict[
            type, tuple[CBVRoutesInfo, Callable[[type[_T]], _T] | None]  # type: ignore
        ] = {}
        self._initialed_state: dict[type[_T], _T] = {}  # type: ignore

    def create_route(
        self,
        *,
        cls: type[_T],
        path: str,
        method: RequestMethod,
        method_name: str,
    ):
        class_routes_info = self._cls_routes_extra[cls][0]

        class_tags = class_routes_info.get("tags") or []
        endpoint_tags: list[str | Enum] = (
            self._state[cls][method_name].get("tags") or []
        )
        tags = class_tags + endpoint_tags

        class_dependencies = class_routes_info.get("dependencies") or []
        endpoint_dependencies = (
            self._state[cls][method_name].get("dependencies") or []
        )
        dependencies = class_dependencies + endpoint_dependencies

        class_responses = class_routes_info.get("responses") or []
        endpoint_responses = (
            self._state[cls][method_name].get("responses") or []
        )
        responses = build_responses(*class_responses, *endpoint_responses)

        status_code = self._state[cls][method_name].get("status")

        deprecated = self._state[cls][method_name].get(
            "deprecated", class_routes_info.get("deprecated")
        )

        response_model = self._state[cls][method_name].get("response_model")

        endpoint_methods = [
            i.upper()
            for i in (self._state[cls][method_name].get("methods") or [method])
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
        methods: list[RequestMethod] | None = None,
        tags: list[str | Enum] | None = None,
        dependencies: list | None = None,
        responses: list[Response] | None = None,
        response_model: type[_T] | None = None,
        status: int | None = None,
        deprecated: bool | None = None,
    ):
        state = self._state
        initial_state = self._initial_state
        data = CBVRouteInfo(
            path=path,
            methods=methods,
            tags=tags,
            dependencies=dependencies,
            responses=responses,
            response_model=response_model,
            status=status,
            deprecated=deprecated,
        )

        def handle(params: DefineMethodParams):
            initial_state(params.method_class)
            deep_merge_dict(
                state,
                {params.method_class: {params.method_name: data}},
            )

        return define_method_handler(handle)

    def _initial_state(self, cls: type[_T]) -> _T:
        if result := self._initialed_state.get(cls):
            return cast(_T, result)

        default_data = {}
        for endpoint in iter_endpoints(cls):
            default_data[endpoint.original_handle_name] = {}

        self._state.setdefault(cls, default_data)
        result = self._build_cls(cls)
        self._initialed_state[cls] = result
        return result

    def _build_cls(self, cls: type[_T]) -> _T:
        if cls in self._cls_routes_extra and (
            build := self._cls_routes_extra[cls][1]
        ):
            return build(cls)  # type: ignore
        return cls()

    def __create_class_dependencies_injector(self, cls: type[_T]):
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

        has_cls_deps = bool(parameters)
        if has_cls_deps:
            update_parameters(collect_cls_dependencies, *parameters)

        def new_fn(method_name, kwargs):
            instance = self._build_cls(cls)
            dependencies = kwargs.pop(collect_cls_dependencies.__name__, {})
            for dep_name, dep_value in dependencies.items():
                setattr(instance, dep_name, dep_value)
            return getattr(instance, method_name)

        def decorator(method: Callable):
            method_name = method.__name__

            cls_fn = getattr(cls, method_name)
            sign_cls_fn = partial(cls_fn)
            update_wrapper(sign_cls_fn, cls_fn)

            if has_cls_deps:
                parameters, *_ = with_parameter(
                    sign_cls_fn,
                    name=collect_cls_dependencies.__name__,
                    default=Depends(collect_cls_dependencies),
                )
            else:
                parameters = list_parameters(sign_cls_fn)

            update_parameters(sign_cls_fn, *(parameters[1:]))

            if inspect.iscoroutinefunction(method):

                @wraps(sign_cls_fn)
                async def awrapper(*args, **kwargs):
                    fn = new_fn(method_name, kwargs)
                    return await fn(*args, **kwargs)

                return awrapper

            @wraps(sign_cls_fn)
            def wrapper(*args, **kwargs):
                fn = new_fn(method_name, kwargs)
                return fn(*args, **kwargs)

            return wrapper

        return decorator

    @overload
    def __call__(self, cls: type[_T], /) -> type[_T]: ...
    @overload
    def __call__(
        self,
        *,
        info: CBVRoutesInfo | None = None,
        build: Callable[[type[_T]], _T] | None = None,
    ) -> Callable[[type[_T]], type[_T]]: ...

    def __call__(self, *args, **kwargs):
        info: CBVRoutesInfo = {}
        build: Callable | None = None

        def decorator(cls: type[_T]) -> type[_T]:
            instance = self._initial_state(cls)
            self._cls_routes_extra[cls] = info, build

            decorator = self.__create_class_dependencies_injector(cls)

            def valid_method(
                name: str, _handle: Callable
            ) -> None | list[_MethodInfo]:
                if (cls_state := self._state.get(cls)) and (
                    method_state := cls_state.get(name)
                ):
                    methods: list[RequestMethod] = (
                        method_state.get("methods") or []
                    )
                    result: list[_MethodInfo] = []
                    for i in methods:
                        method = Methods(i.lower())
                        result.append((method, METHOD_PATTERNS[method]))
                    return result

                return None

            for endpoint_info in iter_endpoints(cls, valid_method):
                route = self.create_route(
                    cls=cls,
                    path=endpoint_info.path,
                    method=endpoint_info.method,
                    method_name=endpoint_info.original_handle_name,
                )
                method = getattr(instance, endpoint_info.original_handle_name)
                endpoint = decorator(method)
                endpoint.__name__ = endpoint_info.handle_name
                route(endpoint)

            return cls

        if args:
            return decorator(args[0])

        info.update(kwargs.get("info") or {})
        build = kwargs.get("build")

        return decorator
