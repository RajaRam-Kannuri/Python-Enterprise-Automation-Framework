from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel
from pydantic.generics import GenericModel

if TYPE_CHECKING:
    from pydantic.typing import DictStrAny


def to_camel_case(string: str) -> str:
    """
    Convert snake_case to camelCase
    """
    words = string.split("_")
    return words[0].lower() + "".join(w.capitalize() for w in words[1:])


class LMSModelBase(BaseModel):
    def lms_dict(self, *, exclude_none=True, exclude_unset=False) -> "DictStrAny":
        return self.dict(by_alias=True, exclude_none=exclude_none, exclude_unset=exclude_unset)

    def lms_json(self, *, exclude_none=True, exclude_unset=False) -> str:
        return self.json(by_alias=True, exclude_none=exclude_none, exclude_unset=exclude_unset)

    class Config:
        alias_generator = to_camel_case
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {datetime: datetime.isoformat}


class LMSEntityModelBase(LMSModelBase):
    id: str


class LMSGenericModelBase(GenericModel):
    def lms_dict(self) -> "DictStrAny":
        return super().dict(by_alias=True, exclude_none=True)

    def lms_json(self) -> str:
        return super().json(by_alias=True, exclude_none=True)

    class Config:
        alias_generator = to_camel_case
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {datetime: datetime.isoformat}


# Some stubs for not fully functional api's
class LMSHasKey(LMSEntityModelBase):
    pass


class LMSMayHasKey(LMSModelBase):
    id: str | None
