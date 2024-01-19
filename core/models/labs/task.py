from typing import List

from pydantic import BaseModel, Field

from core.models.labs.acceptance_criteria import AcceptanceCriteria
from util.random import random_string

DESCRIPTION_TASK = {
    "type": "doc",
    "content": [{"type": "paragraph", "content": [{"text": "This is a description for the task", "type": "text"}]}],
}


class TranslatedTaskInput(BaseModel):
    name: str = Field(default_factory=lambda: random_string(prefix="AUTOTEST_"))
    acceptance_criteria: List[AcceptanceCriteria] = []
    data: dict = DESCRIPTION_TASK


class TranslatedTask(BaseModel):
    """example:
        {
      "id": 9865,
      "name": "task 1",
      "defined_grade": "1.000",
      "acceptance_criteria": [],
      "data": {
        "type": "doc",
        "content": [
          {
            "type": "paragraph",
            "content": [
              {
                "text": "This is a description for the task",
                "type": "text"
              }
            ]
          }
        ]
      },
      "steps": [],
      "labs": [],
      "level": 0
    }
    """

    id: int
    name: str
    acceptance_criteria: List[AcceptanceCriteria]
    data: dict
    steps: list
    defined_grade: str | None = None
    labs: List[str]
    order: int | None = None
    result: str | None = None
    level: int
    translation_coverage: dict | None = None
    translation_language: dict | None = None
    translations: list | None = None


class LabsTaskLinkInputModel(BaseModel):
    lab: int
    order: int | None = None


class LabsTaskLinkModel(BaseModel):
    """example:
        {
      "id": 9870,
      "name": "task 1",
      "acceptance_criteria": [],
      "data": {
        "type": "doc",
        "content": [
          {
            "type": "paragraph",
            "content": [
              {
                "text": "This is a description for the task",
                "type": "text"
              }
            ]
          }
        ]
      },
      "order": 0,
      "steps": [],
      "level": 0,
      "is_content_only": false
    }
    """

    id: int
    acceptance_criteria: AcceptanceCriteria | None = None
    data: dict | None = None
    order: int | None = None
    steps: list[int] = []
    level: int
    is_content_only: str
