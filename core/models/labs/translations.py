from enum import StrEnum

from pydantic import BaseModel


class TranslationContentTypes(StrEnum):
    LAB_DESCRIPTION = "lab.data"
    TASK = "task"
    STEP = "step"
    HINT = "hint"


class AutoTranslation(BaseModel):
    content_type: str
    object_id: str | None
    lab: int | None
    service: int | None
    lang_from: str | None
    lang_to: str | None
    field_name: str | None
    language: str | None
    value: str | None

    @property
    def id(self) -> str:
        return self.object_id


class AutoTranslationInput(BaseModel):
    content_type: str
    object_id: str | None
    lab: int | None
    lang_from: str
    lang_to: str

    @property
    def id(self) -> str:
        return self.object_id


class BackendsTranslation(BaseModel):
    id: int | None
    name: str
    type: str = "azure"


class Translation(BaseModel):
    id: int
    content_type: str
    object_id: str | None
    field_name: str
    lab: int | None
    origin: str
    language: str
    value: str
    approved_at: str | None
    approved_by: int | None


class TranslationInput(BaseModel):
    id: int
    origin: str
    value: str
