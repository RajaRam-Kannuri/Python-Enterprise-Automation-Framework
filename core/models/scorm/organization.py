from datetime import datetime
from enum import Enum, IntEnum

from core.models.lms.lms_base import LMSEntityModelBase, LMSModelBase


class ScormState(IntEnum):
    DRAFT = 1
    READY = 2
    EXPIRED = 3
    ARCHIVED = 4


class DisplayMode(IntEnum):
    FULL_SCREEN = 1
    EMBEDDED_AUTO = 2
    EMBEDDED_CUSTOM = 3


class OrganizationBase(LMSModelBase):
    title: str
    entry_point: str | None
    version: str
    code: str
    description: str | None
    is_internal_image: bool | None
    image_url: str | None
    state: ScormState
    support_review: bool | None = False
    support_mobile_view: bool | None = False
    support_fullscreen_view: bool | None = True
    preferred_width: int | None = None
    preferred_height: int | None = None
    display_mode: DisplayMode = DisplayMode.FULL_SCREEN
    report_progress_as_score: bool | None = False
    show_submit_button: bool | None = True
    show_close_button: bool | None = True


class Organization(OrganizationBase, LMSEntityModelBase):
    id: str
    tenant_id: str
    created: datetime | None
    created_by: str | None
    modified: datetime | None
    modified_by: str | None
    original_file_name: str | None
    original_file_size: int


class UpdateOrganization(OrganizationBase):
    def to_dict(self):
        data = self.dict()
        if isinstance(data["state"], Enum):
            data["state"] = data["state"].value
        return data
