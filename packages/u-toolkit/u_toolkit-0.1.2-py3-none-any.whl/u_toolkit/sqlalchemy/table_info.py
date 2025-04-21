import sqlalchemy as sa
from pydantic import TypeAdapter

from .type_vars import DeclarativeBaseT


class TableInfo:
    def __init__(self, table: type[DeclarativeBaseT]) -> None:
        self.table = table
        self.columns = sa.inspect(table).c
        self.adapters = {
            i.name: (
                TypeAdapter(i.type.python_type),
                i.type.python_type,
            )
            for i in self.columns
        }
