from typing import TypeVar

from sqlalchemy.orm import DeclarativeBase


DeclarativeBaseT = TypeVar("DeclarativeBaseT", bound=DeclarativeBase)
