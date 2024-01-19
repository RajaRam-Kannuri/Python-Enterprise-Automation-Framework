from datetime import datetime
from enum import IntEnum

from core.models.lms.lms_base import LMSModelBase


class CompletionState(IntEnum):
    Completed = 1
    Failed = 2
    Canceled = 3


class Operation(LMSModelBase):
    id: str
    url: str
    message: str


class Completion(LMSModelBase):
    url: str
    completed: datetime
    state: CompletionState
    errors: dict | None


class Command(LMSModelBase):
    id: str
    entity_id: str
    created: datetime
    completed: Completion | None

    def is_completed(self) -> bool:
        return self.completed is not None

    def is_succeeded(self) -> bool:
        return (
            self.completed is not None
            and self.completed.state == CompletionState.Completed
            and not self.completed.errors
        )
