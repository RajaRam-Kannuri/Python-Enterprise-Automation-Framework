from typing import List

from core.models.lms.lms_base import LMSModelBase


class LtiResourceInitModel(LMSModelBase):
    auth_uri: str
    iss: str
    target_link_uri: str
    login_hint: str
    lti_message_hint: str


class LtiResourceLinkModel(LMSModelBase):
    activity_workflow_ids: List[str]
    activity_part_ids: List[str]
