from datetime import datetime

from pydantic.alias_generators import to_snake
from sqlalchemy import func
from sqlalchemy.orm import Mapped, declared_attr, mapped_column


class TablenameMixin:
    # 当继承该类时, 会自动将表名转为 snake 名称形式
    @declared_attr.directive
    @classmethod
    def __tablename__(cls) -> str:
        return f"{to_snake(cls.__name__)}_tb"


class TimeStampMixin:
    # 当继承该类时, 会给表添加创建时间和更新时间字段
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), sort_order=9998
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        onupdate=func.now(), sort_order=9999
    )
