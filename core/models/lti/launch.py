from core.models.lms.lms_base import LMSModelBase


class LaunchForm(LMSModelBase):
    id_token: str
    scope: str
    state: str
    session_state: str
