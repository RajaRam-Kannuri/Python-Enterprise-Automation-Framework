from enum import IntEnum
from typing import Union

from pydantic import Field, confloat

from core.models.lms.lms_base import LMSEntityModelBase, LMSModelBase
from settings import settings
from util.random import random_string, random_text


class ActivityType(IntEnum):
    INITIAL_TYPE = 0  # Default value while starting activity workflow
    TEXT = 1
    LTI = 2
    COMPOSITE = 3
    EVENT = 4
    VIDEO = 5


class ActivityState(IntEnum):
    PARTIALLY_LOADED = 0  # Represents a deliberate design choice to load only a subset of fields from the database
    DRAFT = 1
    READY = 2
    EXPIRED = 3
    ARCHIVED = 4


class PresentationMode(IntEnum):
    TREE = 0
    TILES = 1
    LONG_READ = 2


class LtiVersion(IntEnum):
    LTI11 = 1
    LTI13 = 3


class ActivityBase(LMSModelBase):
    content: str | None = ""
    editor_content: str | None = ""
    lti_version: int | None = None
    tool_resource_id: str | None = ""
    external_id: str | None = None
    name: str | None = Field(default_factory=lambda: random_string(prefix="TestActName-"))
    code: str | None = Field(default_factory=lambda: random_string(prefix="TestCode-"))
    description: str | None = Field(default_factory=random_text)
    support_review: bool = False
    support_lti_grading: bool | None = None
    support_lti_authoring: bool | None = None
    support_mobile_view: bool = True
    support_fullscreen_view: bool = True
    preferred_width: int | None = None
    preferred_height: int | None = None
    recommended_duration: int | None
    recommended_attempts: int | None


class CreateActivity(ActivityBase):
    resource_library_id: str
    state: ActivityState
    type: ActivityType
    tool_url: str = ""
    team_id: str = settings.stand_config.team_id
    tool_auth_url: str | None


class UpdateActivity(ActivityBase):
    resource_library_id: str | None
    tool_url: str | None
    type: ActivityType | None
    tool_auth_url: str | None
    state: ActivityState | None
    image_url: str | None
    is_internal_image: bool | None
    passing_score: confloat(ge=0.0, le=1.0, allow_inf_nan=False) | None
    max_score: float | None
    presentation_mode: PresentationMode | None
    normalized_passing_score: confloat(ge=0.0, le=1.0, allow_inf_nan=False) | None
    proctored: bool | None
    proctoring_settings: str | None
    children: Union["Activity", None]
    team_id: str | None = None


class Activity(UpdateActivity, LMSEntityModelBase):
    state: ActivityState
    id: str


UpdateActivity.update_forward_refs()
Activity.update_forward_refs()
