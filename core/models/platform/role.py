from datetime import datetime

from core.models.platform.base import PlatformModelBase


class UserIdFullName(PlatformModelBase):
    id: str | None = None
    full_name: str


class RoleFields(PlatformModelBase):
    # Simplified role view
    id: str
    name: str
    description: str
    builtin: bool
    application_id: str
    tenant_id: str
    owmner_role_id: str | None = None


class Role(RoleFields):
    created_at: datetime
    created_by: UserIdFullName
    modified_at: datetime | None = None
    modified_by: UserIdFullName | None = None


class UpdateRole(PlatformModelBase):
    name: str
    description: str
    owner_role_id: str | None = None


class CreateRole(UpdateRole):
    id: str | None = None


class RoleAssignedToUser(PlatformModelBase):
    id: str
    role: RoleFields


class RoleWithUserRoleID(PlatformModelBase):
    role: RoleFields
    user_role_id: str
