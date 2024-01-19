from pydantic import BaseModel, Field

from core.models.labs.step_criteria import StepCriteria, StepCriteriaInput
from util.random import random_string

DESCRIPTION_STEP = {
    "type": "doc",
    "content": [{"type": "paragraph", "content": [{"text": "This is a description for the step", "type": "text"}]}],
}


class StepInput(BaseModel):
    name: str = Field(default_factory=lambda: random_string(prefix="AUTOTEST_"))
    acceptance_criteria: list[StepCriteriaInput] | None = []
    data: dict = DESCRIPTION_STEP
    hints: list | None = []


class StepModel(BaseModel):
    id: int
    name: str
    data: dict
    tasks: list
    suggested_inputs: list
    hints: list
    acceptance_criteria: list[StepCriteria]
    is_virtual: bool
    translation_language: str | None
    translations: list | None
    translation_coverage: dict | None


class TaskStepLinkRequestModel(BaseModel):
    order: int | None = None

    # these two parameters are marked as required in a project swagger,
    # but they don't seem to affect anything:

    # step: int
    # task: int


class TaskStepLinkModel(BaseModel):
    """example:
        {
      "id": 33774,
      "name": "OjuDudFrtD",
      "acceptance_criteria": [],
      "data": {
        "type": "doc",
        "content": [
          {
            "type": "paragraph",
            "content": [
              {
                "text": "This is a description for the step",
                "type": "text"
              }
            ]
          }
        ]
      },
      "order": 0,
      "variables_ready": false,
      "is_virtual": false,
      "translations": [],
      "translation_language": "None"
    }
    """

    id: int
    name: str
    acceptance_criteria: list
    data: dict
    order: int
    variables_ready: bool
    is_virtual: bool
    translations: list | None
    translation_language: str | None
