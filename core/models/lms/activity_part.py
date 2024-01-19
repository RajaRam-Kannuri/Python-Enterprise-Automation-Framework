from enum import IntEnum

from core.models.lms.activity import Activity
from core.models.lms.lms_base import LMSEntityModelBase, LMSModelBase


class ControlFlowGate(IntEnum):
    FREE = 1
    PASSING_SCORE = 2


class ActivityPart(LMSEntityModelBase):
    child_activity: Activity
    id: str
    order: int
    parent_activity_id: str
    child_activity_id: str
    allowed_attempts: int | None
    gate: ControlFlowGate
    progress_weight: float
    score_weight: float
    normalized_passing_score: float


class CreateActivityPart(LMSModelBase):
    id: str | None = None
    parent_activity_id: str
    child_activity_id: str
    team_id: str | None = None
    order: int = 0
    allowed_attempts: int | None = None
    score_weight: float | None = 1.0
    progress_weight: float | None = 1.0
    gate: ControlFlowGate = ControlFlowGate.FREE


class UpdateActivityPart(LMSModelBase):
    child_activity_id: str
    child_activity: Activity
    team_id: str | None = None
    order: int | None = None
    score_weight: float | None = None
    gate: ControlFlowGate | None = None
    allowed_attempts: int | None = None
    normalized_passing_score: float | None = None


class CreateActivityPartFromResource(LMSModelBase):
    id: str | None = None
    team_id: str | None = None
    resource_library_id: str
    resource_id: str
    parent_activity_id: str
    order: int = 0
    allowed_attempts: int | None = None
    gate: ControlFlowGate = ControlFlowGate.FREE
    score_weight: float | None = 1.0
    progress_weight: float | None = 1.0
    normalizedPassingScore: float | None = None
