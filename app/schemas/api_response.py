from typing import (
    Any,
    Generic,
    TypeVar,
)

from pydantic import (
    BaseModel,
    Field,
)


TData = TypeVar("TData")


class ApiResponseSchema(BaseModel, Generic[TData]):
    data: TData | dict = Field(default_factory=dict)
    meta: dict[str, Any] = Field(default_factory=dict)
    errors: list[Any] = Field(default_factory=list)
