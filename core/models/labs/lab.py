from enum import StrEnum
from typing import List

from pydantic import BaseModel, Field

from core.models.labs.acceptance_criteria import AcceptanceCriteria
from core.models.labs.actions import SessionAction
from core.models.labs.variable_template import VariableTemplateLabLink, VariableTemplateLabLinkPK
from core.models.labs.workspace_configuration import ComponentType
from util.random import random_string


class PreviousLab(BaseModel):
    id: int
    name: str


class ActionType(StrEnum):
    RESET = "reset"
    AFTER = "after"
    START = "start"
    FINISH = "finish"
    INREVIEW = "inreview"


class TargetState(StrEnum):
    PREPARED = "prepared"
    ACTIVE = "active"
    FINISHED = "finished"
    INREVIEW = "inreview"
    PAUSED = "paused"
    CLEANED = "cleaned"


class LabSessionActionLink(BaseModel):
    action: SessionAction
    type: ActionType
    target_state: TargetState


class LabSessionActionLinkPK(BaseModel):
    action: int
    type: ActionType
    target_state: TargetState


class LabDetailed(BaseModel):
    """example =
    {
        "acceptance_criteria": null,
        "actions": [],
        "check_for_plagiarism": false,
        "code": "LAB-4014",
        "contacts": [],
        "created_at": "2023-08-09T13:39:58.916151Z",
        "created_by": {
            "email": "autotest@alemira.dev",
            "first_name": "Test",
            "id": 1866,
            "last_name": "Testovich",
            "locale": null,
            "picture_url": ""
        },
        "data": null,
        "default_language": "en-US",
        "default_type": "virtual_machine",
        "description_html": null,
        "edit_url": "/labs/virtual-labs/4014",
        "enable_terminal": false,
        "id": 4014,
        "is_coding_multi": false,
        "is_public": false,
        "labels": [],
        "languages": [],
        "limit_seconds": 3600,
        "links": [],
        "logo_link": "",
        "lti_1p3_url": "/labs/api/lti1p3/4014",
        "lti_object_id": 4014,
        "lti_url": "/labs/api/lti/4014",
        "manual_assessment": false,
        "name": "Virtual environment lab",
        "next_active": [],
        "next_ids": [],
        "organization": "org-mfyir3gna",
        "pregeneratevariables": [],
        "preview_mode": false,
        "previous": null,
        "publish_updated_at": null,
        "related_labs_vars": [],
        "sequential_walkthrough_order": true,
        "status": "draft",
        "suggested_inputs": [
            "vle_player_host",
            "vle_vm_session_token",
            "vle_vm_session_id",
            "vle_locale",
            "vle_username"
        ],
        "suspend_after_seconds_inactivity": 1800,
        "tasks": [],
        "updated_at": "2023-08-09T13:39:58.916177Z",
        "updated_by": null,
        "workspace_configuration": "wcfg-f97ui9uo3"
    }"""

    acceptance_criteria: AcceptanceCriteria | None = None
    actions: list[LabSessionActionLink] = []
    check_for_plagiarism: bool = False
    code: str
    contacts: list = []
    created_at: str
    created_by: dict
    data: dict | None = None
    default_language: str
    default_type: ComponentType
    description_html: str | None = None
    edit_url: str
    enable_terminal: bool = False
    id: int
    is_coding_multi: bool = False
    is_public: bool = False
    labels: list = []
    languages: list = []
    limit_seconds: int = 3600
    links: list = []
    logo_link: str
    lti_1p3_url: str
    lti_object_id: int
    lti_url: str
    manual_assessment: bool = False
    name: str
    next_active: list = []
    next_ids: list = []
    organization: str
    pregeneratevariables: List[VariableTemplateLabLink] = []
    preview_mode: bool = False
    previous: PreviousLab | None = None
    publish_updated_at: str | None = None
    related_labs_vars: list | None = None
    sequential_walkthrough_order: bool = True
    status: str
    suggested_inputs: list = []
    suspend_after_seconds_inactivity: int | None = None
    tasks: list = []
    updated_at: str
    updated_by: dict | None = None
    workspace_configuration: str
    translation_coverage: dict | None = None


class LabInput(BaseModel):
    name: str = Field(default_factory=lambda: random_string(prefix="AUTOTEST_"))
    contacts: list = []
    links: list = []
    previous_id: str = None
    acceptance_criteria: AcceptanceCriteria | None = None
    data: dict | None = None
    logo_link: str = ""
    is_public: bool = False
    default_type: ComponentType = ComponentType.VIRTUAL_MACHINE
    limit_seconds: int = 720
    suspend_after_seconds_inactivity: int = 720
    manual_assessment: bool = False
    sequential_walkthrough_order: bool = True
    check_for_plagiarism: bool = False
    enable_terminal: bool = False
    workspace_configuration: str
    actionlinks: list[LabSessionActionLinkPK] = []
    pregenvariables: List[VariableTemplateLabLinkPK] = []
    default_language: str = "en-US"
    label_ids: list = []
