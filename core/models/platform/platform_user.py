from datetime import date
from enum import StrEnum

from faker import Faker
from pydantic import Field

from core.models.platform.base import PlatformModelBase
from core.models.platform.role import RoleWithUserRoleID

faker = Faker("en_US")


class PlatformUserStatus(StrEnum):
    CREATED = "Created"
    ACTIVE = "Active"
    SUSPENDED = "Suspended"
    ARCHIVED = "Archived"


class PlatformUserDepartment(PlatformModelBase):
    id: str | None
    name: str | None
    title: str | None


class PlatformUserShort(PlatformModelBase):
    id: str
    username: str
    email: str
    first_name: str
    last_name: str
    middle_name: str | None = None
    external_id: str | None = None
    phone_number: str | None = None
    hired: date | None = None
    retired: date | None = None
    tenant_id: str
    is_blocked: bool
    status: PlatformUserStatus


class PlatformUser(PlatformUserShort):
    department: PlatformUserDepartment | None = None


class UpdatePlatformUser(PlatformModelBase):
    username: str
    email: str
    password: str | None
    first_name: str = Field(default_factory=lambda: f"Auto {faker.first_name()}")
    middle_name: str | None = None
    last_name: str = Field(default_factory=lambda: f"Auto {faker.last_name()}")
    external_id: str | None = None
    phone_number: str | None = None
    hired: date | None = None
    retired: date | None = None


class CreatePlatformUser(UpdatePlatformUser):
    id: str | None = None


class UserWithUserRoleId(PlatformModelBase):
    user: PlatformUserShort
    user_role_id: list[RoleWithUserRoleID]


class UserData(PlatformModelBase):
    firstName: str | None
    fullName: str
    id: str
    lastName: str | None
