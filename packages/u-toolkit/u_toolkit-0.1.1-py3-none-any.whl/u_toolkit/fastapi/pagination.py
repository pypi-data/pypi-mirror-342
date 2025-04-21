from collections.abc import Sequence
from math import ceil
from typing import Annotated, Generic, overload

from fastapi import Depends, Query
from pydantic import BaseModel, Field, NonNegativeInt, PositiveInt
from sqlalchemy import MappingResult, ScalarResult

from u_toolkit.pydantic.type_vars import BaseModelT
from u_toolkit.sqlalchemy.type_vars import DeclarativeBaseT


class Page(BaseModel, Generic[BaseModelT]):
    page_size: PositiveInt = Field(description="page size")
    page_no: PositiveInt = Field(description="page number")

    page_count: NonNegativeInt = Field(description="page count")
    count: NonNegativeInt = Field(description="result count")

    results: list[BaseModelT] = Field(description="results")


class PageParamsModel(BaseModel):
    page_size: int = Query(
        50,
        ge=1,
        le=100,
        description="page size",
    )
    page_no: PositiveInt = Query(
        1,
        description="page number",
    )


PageParams = Annotated[PageParamsModel, Depends()]


@overload
def page(
    model_class: type[BaseModelT],
    pagination: PageParamsModel,
    count: int,
    results: ScalarResult[DeclarativeBaseT],
) -> Page[BaseModelT]: ...


@overload
def page(
    model_class: type[BaseModelT],
    pagination: PageParamsModel,
    count: int,
    results: MappingResult,
) -> Page[BaseModelT]: ...


@overload
def page(
    model_class: type[BaseModelT],
    pagination: PageParamsModel,
    count: int,
    results: Sequence[DeclarativeBaseT],
) -> Page[BaseModelT]: ...


def page(
    model_class: type[BaseModelT],
    pagination: PageParamsModel,
    count: int,
    results,
) -> Page[BaseModelT]:
    results_ = [model_class.model_validate(i) for i in results]
    return Page(
        page_size=pagination.page_size,
        page_no=pagination.page_no,
        page_count=ceil(count / pagination.page_size),
        count=count,
        results=results_,  # type: ignore
    )
