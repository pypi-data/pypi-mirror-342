from typing import Annotated, get_origin


def is_annotated(target):
    return get_origin(target) is Annotated
