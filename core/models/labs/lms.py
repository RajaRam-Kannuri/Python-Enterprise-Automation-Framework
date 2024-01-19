from pydantic import BaseModel, Field

from util.random import random_string


class LmsOrganisationInput(BaseModel):
    name: str = Field(default_factory=lambda: random_string(prefix="AUTOTEST_"))


class LmsOrganisation(BaseModel):
    id: str
    name: str
    client_secret: str
    organization: str
