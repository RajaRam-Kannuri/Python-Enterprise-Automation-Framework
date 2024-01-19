from pydantic import Field

from core.models.lms.activity import Activity
from core.models.lms.lms_base import LMSEntityModelBase, LMSModelBase
from core.models.platform.tenant import Tenant
from util.random import random_string, random_text


class ObjectiveBase(LMSModelBase):
    name: str = Field(default_factory=lambda: random_string(prefix="TestObjName-"))
    code: str = Field(default_factory=lambda: random_string(prefix="TestCode-"))
    about: str | None = None
    about_content: str | None = None
    description: str | None = Field(default_factory=lambda: random_text(256))
    external_id: str | None = None
    image_url: str | None = None
    is_internal_image: bool = False


class Objective(ObjectiveBase, LMSEntityModelBase):
    id: str
    activity: Activity | None
    tenant: Tenant | None


class UpdateObjective(ObjectiveBase):
    pass


class CreateObjective(UpdateObjective):
    id: str | None = None
    activity_id: str
