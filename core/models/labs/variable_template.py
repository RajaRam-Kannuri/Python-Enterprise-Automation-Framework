from pydantic import BaseModel, Field

from util.random import random_string


class VariableTemplateInput(BaseModel):
    """
    example = {"name":"vle_username","value":"somename"}
    name cannot start with a number
    """

    name: str = Field(default_factory=lambda: random_string(15, prefix="var_"))
    value: str = Field(default_factory=random_string)


class VariableTemplate(BaseModel):
    """
    example = {"name":"vle_username","value":"somename", "id": 70}
    """

    id: int
    name: str
    value: str


class VariableTemplateLabLinkPK(BaseModel):
    template: int
    varname: str | None


class VariableTemplateLabLink(BaseModel):
    template: VariableTemplate
    varname: str | None

    def to_input_type(self) -> VariableTemplateLabLinkPK:
        return VariableTemplateLabLinkPK(template=self.template.id, varname=self.varname)
