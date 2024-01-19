from datetime import date

from core.models.platform.base import PlatformModelBase
from core.models.platform.platform_user import PlatformUser


class UpdateGroup(PlatformModelBase):
    name: str
    code: str | None = None
    description: str | None = None
    external_id: str | None = None


class CreateGroup(UpdateGroup):
    id: str | None = None


class Group(PlatformModelBase):
    id: str
    name: str
    tenant_id: str
    application_id: str
    code: str | None = None
    description: str | None = None
    external_id: str | None = None


class UserMembershipInGroup(PlatformModelBase):
    id: str
    external_id: str | None = None
    finished: date | None = None
    started: date | None = None


class UserWithGroupMembership(PlatformModelBase):
    membership: list[UserMembershipInGroup]
    user: PlatformUser
