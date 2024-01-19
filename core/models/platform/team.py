from core.models.platform.base import PlatformModelBase


class Team(PlatformModelBase):
    id: str
    name: str
    application_id: str | None
    tenant_id: str | None
    description: str | None = None


class UpdateTeam(PlatformModelBase):
    name: str
    description: str | None = None


class CreateTeam(UpdateTeam):
    id: str | None = None
