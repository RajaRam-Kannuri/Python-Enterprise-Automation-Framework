from datetime import datetime

from core.models.platform.base import PlatformModelBase


class PermissionFields(PlatformModelBase):
    application_id: str
    builtin: bool
    description: str
    id: str
    name: str
    scope_id: str | None = None
    scope_type: str | None = None
    tenant_id: str


class Permission(PermissionFields):
    created_at: datetime
    created_by: str


class CreatePermission(PlatformModelBase):
    id: str | None = None
    name: str
    description: str
    scope_type: str | None = None
    scope_id: str | None = None


class PermissionAssignedToRole(PlatformModelBase):
    id: str
    permission: PermissionFields
