from collections.abc import Callable
from functools import wraps
from typing import Generic, NamedTuple, TypeVar

from u_toolkit.signature import list_parameters, update_parameters


_FnT = TypeVar("_FnT", bound=Callable)

_T = TypeVar("_T")


class DefineMethodParams(NamedTuple, Generic[_T, _FnT]):
    method_class: type[_T]
    method_name: str
    method: _FnT


class DefineMethodDecorator(Generic[_T, _FnT]):
    def __init__(self, fn: _FnT):
        self.fn = fn
        self.name = fn.__name__

    def register_method(self, params: DefineMethodParams[_T, _FnT]): ...

    def __set_name__(self, owner_class: type, name: str):
        self.register_method(DefineMethodParams(owner_class, name, self.fn))

    def __get__(self, instance: _T, owner_class: type[_T]):
        parameters = list_parameters(self.fn)[1:]
        update_parameters(self.fn, *parameters)

        @wraps(self.fn)
        def wrapper(*args, **kwargs):
            return self.fn(instance, *args, **kwargs)

        return wrapper


def define_method_handler(
    handle: Callable[[DefineMethodParams[_T, _FnT]], None],
):
    class Decorator(DefineMethodDecorator):
        def register_method(self, params: DefineMethodParams):
            handle(params)

    return Decorator
