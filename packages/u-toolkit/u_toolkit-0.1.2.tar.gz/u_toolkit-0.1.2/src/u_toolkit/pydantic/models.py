from datetime import datetime
from typing import Annotated, Any

from pydantic import BaseModel, ConfigDict, WrapSerializer

from u_toolkit.alias_generators import to_camel
from u_toolkit.datetime import to_utc

from .type_vars import BaseModelT


class Model(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )


class CamelModel(Model):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
        field_title_generator=to_camel,
    )


def convert_to_utc(value: Any, handler, info) -> dict[str, datetime]:
    # Note that `helper` can actually help serialize the `value` for
    # further custom serialization in case it's a subclass.
    partial_result = handler(value, info)
    if info.mode == "json":
        return {
            k: to_utc(datetime.fromisoformat(v))
            for k, v in partial_result.items()
        }

    return {k: to_utc(v) for k, v in partial_result.items()}


ConvertToUTCModel = Annotated[BaseModelT, WrapSerializer(convert_to_utc)]
