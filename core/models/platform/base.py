from typing import Generic, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T")


class PlatformModelBase(BaseModel):
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class PlatformGenericModelBase(GenericModel):
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class Pagination(PlatformModelBase):
    has_next: bool
    next_page: str


class PlatformListModel(PlatformGenericModelBase, Generic[T]):
    items: list[T]
    pagination: Pagination
