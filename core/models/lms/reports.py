from core.models.lms.activity import Activity, ActivityState, ActivityType
from core.models.lms.lms_base import LMSEntityModelBase
from core.models.lms.lms_user import User
from core.models.lms.objective_workflow_aggregate import WorkflowState
from core.models.lms.proctoring_session import ProctoringSession


class ActivityInfo(LMSEntityModelBase):
    type: ActivityType
    code: str | None
    name: str | None
    state: ActivityState
    proctored: bool


class ObjectiveInfo(LMSEntityModelBase):
    activity: ActivityInfo
    code: str
    name: str
    image_url: str | None
    is_internal_image: bool


class ObjectiveReports(LMSEntityModelBase):
    objective: ObjectiveInfo
    total_enrolled_count: int
    not_started_count: int
    in_progress_count: int
    completed_count: int
    cheated_count: int
    passed_count: int
    average_score: float | None


class ActivityPartReportModel(LMSEntityModelBase):
    parent_id: str | None
    natural_id: str
    natural_parent_id: str | None
    order: int
    has_children: bool
    activity: ActivityInfo
    total_enrolled_count: int
    not_started_count: int
    in_progress_count: int
    completed_count: int
    cheated_count: int
    passed_count: int
    average_score: float | None


class GradingReports(LMSEntityModelBase):
    activity_id: str
    user_id: str
    tenant_id: str
    state: WorkflowState
    created: str
    submitted: str | None
    graded: str | None
    graded_user_id: str | None
    graded_user_last_name: str | None
    graded_user_email: str | None
    graded_user_first_name: str | None
    graded_user_middle_name: str | None
    graded_user_external_id: str | None
    grade_approved: str | None
    grade_approved_user_id: str | None
    grade_approved_user_last_name: str | None
    grade_approved_user_email: str | None
    grade_approved_user_first_name: str | None
    grade_approved_user_middle_name: str | None
    grade_approved_user_external_id: str | None
    grade: str | None
    score: float | None
    user: User
    activity: Activity
    activity_record_id: str | None
    activity_workflow_id: str
    group: str
    due_date: str | None
    proctoring_session: ProctoringSession
