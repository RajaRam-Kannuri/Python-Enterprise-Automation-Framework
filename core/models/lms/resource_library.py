from enum import IntEnum, StrEnum

from core.models.lms.activity import ActivityBase, ActivityState, ActivityType, LtiVersion
from core.models.lms.lms_base import LMSEntityModelBase, LMSModelBase
from core.models.platform.platform_user import UserData
from core.models.platform.team import Team
from core.models.scorm.organization import DisplayMode


class ResourceLibraryType(IntEnum):
    Lti13 = 1
    PublicFile = 2
    PrivateFile = 3
    Lti11 = 4
    Text = 5
    Composite = 6
    Vimeo = 7


class ResourceLibraryBuiltinType(IntEnum):
    NoType = 0
    VirtualLabs = 1
    CodingLabs = 2
    Stem = 3
    PrivateFiles = 4
    PublicFiles = 5
    RichText = 6
    Composite = 7
    JupyterLabs = 8
    Scorm = 9
    Assessment = 10
    Quizzes = 11


class ResourceLibraryName(StrEnum):
    RichText = "Rich Text"
    SCORM = "SCORM"
    STEM_Course = "STEM Course"
    Virtual_Labs = "Virtual Labs"
    Coding_Labs = "Coding Labs"
    Compositions = "Compositions"
    Jupyter_Labs = "Jupyter Labs"
    Quizzes = "Quizzes"


class ResourceLibraryBase(LMSModelBase):
    name: str
    image_url: str | None
    is_builtin_type: bool
    url: str | None
    actions_api_url: str | None
    consumer_key: str | None
    secret_key: str | None
    support_review: bool
    support_lti_grading: bool | None
    support_lti_authoring: bool | None
    bucket_name: str | None
    subfolder: str | None
    user: str | None
    password: str | None
    allow_publishing: bool
    allow_editing: bool
    support_resource_level_Setting: bool
    support_mobile_view: bool
    support_fullscreen_view: bool
    preferred_width: int | None
    preferred_height: int | None
    auth_url: str | None
    tool_auth_url: str | None
    remote_url: str | None


class UpdateResourceLibrary(ResourceLibraryBase):
    name: str | None


class CreateResourceLibrary(ResourceLibraryBase):
    type: ResourceLibraryType
    builtin_type: ResourceLibraryBuiltinType


class ResourceLibrary(LMSEntityModelBase, CreateResourceLibrary):
    can_edit_builtin_settings: bool


class ResourceLibraryAction(LMSModelBase):
    name: str | None
    url: str | None
    image_url: str | None
    is_lti: bool | None
    lti_role: str | None


class ResourceLibraryActivity(ActivityBase):
    pass


class Resource(LMSModelBase):
    id: str
    activityId: str | None
    name: str
    description: str | None
    publish_url: str | None
    image_url: str | None
    edit_url: str
    lti_version: LtiVersion | None
    support_lti_edit: bool | None
    last_modified: str | None
    code: str
    modified_by: UserData | None
    created_by: UserData | None
    state: ActivityState
    auth_url: str | None
    support_review: bool
    support_lti_grading: bool | None
    support_mobile_view: bool
    support_full_screen_view: bool | None
    display_mode: DisplayMode
    preferred_width: int | None
    preferred_height: int | None
    activity_type: ActivityType | None
    type: str | None
    max_score: int | None
    passing_score: int | None
    attempts: int | None
    duration: int | None
    team: Team | None
