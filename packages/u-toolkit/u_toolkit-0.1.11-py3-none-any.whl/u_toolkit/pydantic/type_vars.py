from typing import TypeVar

from pydantic import BaseModel


BaseModelT = TypeVar("BaseModelT", bound=BaseModel)
