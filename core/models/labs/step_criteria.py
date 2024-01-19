from enum import StrEnum

from pydantic import BaseModel


class CriteriaType(StrEnum):
    API_BASED = "templated_request"
    SCRIPT_BASED = "ssh_script"
    SELENIUM = "selenium_request"
    REQUEST = "request"


class RsBody(BaseModel):
    field: str
    operator: str
    value: str
    logic_prefix: str | None


class RequestAC(BaseModel):
    rs_body: list[RsBody]
    template: int | None


class StepCriteria(BaseModel):
    id: int
    request_test: RequestAC | None
    description: str | None
    type: CriteriaType
    order: int
    selenium_test: int | None
    script_project: int | None
    step: int | None
    component: int | None


class StepCriteriaInput(BaseModel):
    type: CriteriaType
    request_test: RequestAC | None


class StepWithTaskCriteria(StepCriteria):
    task: int | None
    step_is_virtual: bool | None


class StepWithTaskCriteriaInput(BaseModel):
    type: CriteriaType
    task: int | None
    step: int | None
