from core.models.platform.base import PlatformModelBase


class Tenant(PlatformModelBase):
    id: str
    name: str | None
