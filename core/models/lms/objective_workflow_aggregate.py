from enum import IntEnum

from core.models.lms.lms_base import LMSEntityModelBase
from core.models.lms.lms_user import User
from core.models.lms.objective import Objective


class ObjectiveAccess(LMSEntityModelBase):
    id: str
    objective_id: str
    user: str | None
    tenant_id: str
    due_date: str | None
    availability_date: str | None
    availability_end_date: str | None
    retake: bool | None
    is_mandatory: bool | None
    created: str
    modified: str | None


class ObjectiveRecord(LMSEntityModelBase):
    id: str
    objective: Objective | None
    created: str
    started: str
    submitted: str
    finished: str | None
    score: float
    progress: float
    max_score: float
    normalized_score: float
    passed: bool
    grade: str | None
    user: User | None
    objective_workflow_id: str | None
    duration: str
    objective_access: ObjectiveAccess | None


class WorkflowState(IntEnum):
    IN_PROGRESS = 1
    SUBMITTED = 2
    IN_GRADING = 3
    GRADED = 4
    GRADING_APPROVED = 5
    FINISHED = 6


class ObjectiveWorkflow(LMSEntityModelBase):
    id: str
    objective_id: str
    user_id: str
    tenant_id: str
    state: WorkflowState
    created: str
    started: str
    submitted: str | None
    graded: str | None
    grade_approved: str | None
    finished: str | None
    grade: str | None
    score: float | None
    progress: float | None
    user: User | None
    objective: Objective | None
    objective_record_id: str | None
    group: str | None


class ObjectiveWorkflowAggregate(LMSEntityModelBase):
    id: str
    objective: Objective
    objective_access: ObjectiveAccess
    last_objective_record: ObjectiveRecord | None
    last_objective_workflow: ObjectiveWorkflow | None
    has_access: bool | None
    due_date: str | None
    availability_date: str | None
    availability_end_date: str | None
    retake: bool | None
    is_self_enrolled: bool | None
    user_id: str
    has_workflow: bool | None
    is_archived: bool


class StartObjectiveWorkflow(LMSEntityModelBase):
    id: str | None
    objective_workflow_aggregate_id: str


class FinishObjectiveWorkflow(LMSEntityModelBase):
    id: str | None
    objective_workflow_id: str
