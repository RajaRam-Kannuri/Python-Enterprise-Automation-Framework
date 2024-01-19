from datetime import datetime

from core.models.platform.base import PlatformModelBase
from core.models.platform.role import UserIdFullName


class UserRole(PlatformModelBase):
    id: str
    role_id: str
    user_id: str
    created_at: datetime
    created_by: UserIdFullName
    tenant_id: str
    application_id: str


class CreateUserRole(PlatformModelBase):
    id: str | None = None
    role_id: str
    user_id: str
