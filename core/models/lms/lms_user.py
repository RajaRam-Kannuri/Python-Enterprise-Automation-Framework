from core.models.lms.lms_base import LMSEntityModelBase
from core.models.platform.tenant import Tenant


class User(LMSEntityModelBase):
    id: str
    email: str
    username: str
    first_name: str
    middle_name: str | None
    last_name: str
    external_id: str | None
    tenant: Tenant | None
