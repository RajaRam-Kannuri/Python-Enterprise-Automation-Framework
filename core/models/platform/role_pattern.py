from core.models.platform.base import PlatformModelBase
from core.models.platform.permission import PermissionFields


class RolePattern(PlatformModelBase):
    id: str
    kind: int
    name_pattern: str
    description: str
    builtin: bool
    owner_role_id: str | None = None
    owner_role_pattern_id: str | None = None
    scope_type: str
    tenant_id: str
    application_id: str


class RolePatternPermission(PlatformModelBase):
    id: str
    permission: PermissionFields
    role_pattern: RolePattern
    tenant_id: str
    application_id: str
    builtin: bool
