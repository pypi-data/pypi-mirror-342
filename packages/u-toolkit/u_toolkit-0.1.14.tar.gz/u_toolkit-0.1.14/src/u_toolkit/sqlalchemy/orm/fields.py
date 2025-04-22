from functools import partial
from typing import Annotated
from uuid import UUID, uuid4

from sqlalchemy import BIGINT
from sqlalchemy.orm import mapped_column


primary_key_column = partial(mapped_column, primary_key=True, sort_order=-9999)

IntPrimaryKey = Annotated[int, primary_key_column()]
BigIntPrimaryKey = Annotated[int, primary_key_column(BIGINT)]

_auto_pk = partial(primary_key_column, autoincrement=True)

AutoIntPrimaryKey = Annotated[int, _auto_pk()]
AutoBigIntPrimaryKey = Annotated[int, _auto_pk(BIGINT)]


UUID4PrimaryKey = Annotated[UUID, primary_key_column(default=uuid4)]
