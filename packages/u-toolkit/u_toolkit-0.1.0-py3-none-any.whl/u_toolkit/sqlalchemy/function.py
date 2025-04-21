import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, QueryableAttribute


def json_object_build(
    label: str,
    table: type[DeclarativeBase],
    *attrs: QueryableAttribute | sa.Column,
):
    return sa.func.json_build_object(
        *[sa.text(f"'{i.key}', {table.__tablename__}.{i.key}") for i in attrs]
    ).label(label)
