import inspect
from collections.abc import Callable, Sequence
from typing import Annotated, Any, overload


def list_parameters(fn: Callable, /) -> list[inspect.Parameter]:
    signature = inspect.signature(fn)
    return list(signature.parameters.values())


@overload
def with_parameter(
    fn: Callable, *, name: str, annotation: type | Annotated
) -> tuple[list[inspect.Parameter], inspect.Parameter, int]: ...
@overload
def with_parameter(
    fn: Callable, *, name: str, default: Any
) -> tuple[list[inspect.Parameter], inspect.Parameter, int]: ...
@overload
def with_parameter(
    fn: Callable, *, name: str, annotation: type | Annotated, default: Any
) -> tuple[list[inspect.Parameter], inspect.Parameter, int]: ...


def with_parameter(
    fn: Callable,
    *,
    name: str,
    annotation: type | Annotated | None = None,
    default: Any = None,
) -> tuple[list[inspect.Parameter], inspect.Parameter, int]:
    kwargs = {}
    if annotation is not None:
        kwargs["annotation"] = annotation
    if default is not None:
        kwargs["default"] = default

    parameters = list_parameters(fn)
    parameter = inspect.Parameter(
        name=name, kind=inspect.Parameter.KEYWORD_ONLY, **kwargs
    )
    index = -1
    if parameters and parameters[index].kind == inspect.Parameter.VAR_KEYWORD:
        parameters.insert(index, parameter)
        index = -2
    else:
        parameters.append(parameter)

    return parameters, parameter, index


def update_signature(
    fn: Callable,
    *,
    parameters: Sequence[inspect.Parameter] | None = None,
    return_annotation: type | None = None,
):
    signature = inspect.signature(fn)
    if parameters is not None:
        signature = signature.replace(parameters=parameters)
    if return_annotation is not None:
        signature = signature.replace(return_annotation=return_annotation)

    setattr(fn, "__signature__", signature)


def update_parameters(fn: Callable, *parameters: inspect.Parameter):
    update_signature(fn, parameters=parameters)


def update_return_annotation(fn: Callable, return_annotation: type, /):
    update_signature(fn, return_annotation=return_annotation)
