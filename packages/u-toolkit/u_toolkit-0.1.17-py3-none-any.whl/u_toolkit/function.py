from collections.abc import Callable


def get_name(fn: Callable, /):
    return fn.__name__


def add_document(fn: Callable, document: str, /):
    if fn.__doc__ is None:
        fn.__doc__ = document
    else:
        fn.__doc__ += f"\n\n{document}"
