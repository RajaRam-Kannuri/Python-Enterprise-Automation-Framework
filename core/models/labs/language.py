from pydantic import BaseModel


class LabLanguage(BaseModel):
    code: str
    default_name: str
    original_name: str | None
    is_active: bool | None

    @property
    def id(self) -> str:
        return self.code


class LabLanguageInput(BaseModel):
    """
    example = {"lang_code": "de-DE"}
    """

    language_code: str = "de-DE"
