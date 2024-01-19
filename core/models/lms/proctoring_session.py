from enum import IntEnum

from core.models.lms.lms_base import LMSEntityModelBase, LMSModelBase


class ProctoringSessionState(IntEnum):
    NOT_STARTED = 0
    CREATED = 1
    FINISHED = 2


class ThresholdModel(LMSModelBase):
    attention: int | None
    rejected: int | None


class SyntheticState(IntEnum):
    BLANK = 0  # session is null
    IN_PROGRESS = 1  # Cheated == null & & WorkflowState >= InProgress
    FAILED = 2  # Cheated == true
    PASSED = 3  # Cheated == false
    UNKNOWN = 4  # Cheated == null & & State == Finished


class ProctoringSession(LMSEntityModelBase):
    score: int | None
    cheated: bool | None
    state: ProctoringSessionState
    explicit_finish: bool
    reviews_number: bool
    last_review_reported: str | None
    threshold: ThresholdModel
    result_state: SyntheticState
