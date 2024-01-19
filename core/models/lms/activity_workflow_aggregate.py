from core.models.lms.activity import Activity, ActivityState, ActivityType, PresentationMode
from core.models.lms.activity_part import ActivityPart
from core.models.lms.lms_base import LMSEntityModelBase, LMSModelBase
from core.models.lms.lms_user import User
from core.models.lms.objective_workflow_aggregate import WorkflowState


class ActivityRecord(LMSEntityModelBase):
    score: float
    progress: float
    max_score: float
    normalized_score: float
    grade: str | None
    created: str
    started: str
    submitted: str
    finished: str
    activity: Activity | None
    user: User | None
    activity_workflow_id: str | None


class ActivityRecordReduced(LMSEntityModelBase):
    id: str
    score: float
    max_score: float
    normalized_score: float
    grade: str | None
    grade_color: str | None
    started: str
    finished: str


class ActivityWorkflow(LMSEntityModelBase):
    id: str
    activity_id: str
    user_id: str
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
    activity: Activity | None
    activity_record_id: str | None
    last_proctoring_session_id: str | None


class StartActivityWorkflow(LMSModelBase):
    objective_workflow_id: str
    activity_part_ids: list[str] | None


class ActivityWorkflowAggregate(LMSEntityModelBase):
    id: str
    activity: Activity | None
    last_activity_record: ActivityRecord | None
    best_activity_record: ActivityRecord | None
    last_activity_workflow: ActivityWorkflow
    activity_records_count: int
    user_id: str
    children: list["ActivityWorkflowAggregate"] | None  # Refer to the model itself


class FinishActivityWorkflow(LMSModelBase):
    objective_workflow_id: str
    activity_workflow_ids: list[str]


class ActivityWorkflowReduced(LMSEntityModelBase):
    id: str
    state: WorkflowState
    started: str
    finished: str | None
    progress: float | None
    last_proctoring_session_id: str | None


class ActivityWorkflowAggregateReduced(LMSEntityModelBase):
    id: str
    best_activity_record_score: float | None
    last_activity_workflow: ActivityWorkflowReduced
    last_activity_record: ActivityRecordReduced
    activity_records_count: int


class ActivityWithAggregate(LMSEntityModelBase):
    id: str
    type: ActivityType
    code: str
    name: str
    image_url: str | None
    max_score: float | None
    state: ActivityState
    proctored: bool | None
    presentation_mode: PresentationMode
    activity_workflow_aggregate: ActivityWorkflowAggregateReduced
    children: list[Activity] | list[None]
    children_count: int


class ActivityByObjectiveWorkflowAndAxis(LMSEntityModelBase):
    activity_workflow_aggregate: ActivityWorkflowAggregate | None
    activity_part: ActivityPart | None
    activity: Activity | None
