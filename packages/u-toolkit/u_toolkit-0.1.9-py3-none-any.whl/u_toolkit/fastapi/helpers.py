from typing import Annotated, Any, get_args

from fastapi.params import Depends


def is_depend(value: Any):
    return isinstance(value, Depends)


def get_depend_from_annotation(annotation: Annotated):
    args = list(get_args(annotation))
    # 因为 FastAPI 好像也是取最后的依赖运行的, 所以这里也将参数反转
    args.reverse()
    for arg in args:
        if is_depend(arg):
            return arg

    raise ValueError
