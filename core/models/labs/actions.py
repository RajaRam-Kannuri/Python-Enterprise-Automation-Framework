from pydantic import BaseModel, Field

from util.random import random_string


class SessionActionInput(BaseModel):
    data: list = []
    description: str = ""
    name: str = Field(default_factory=lambda: random_string(prefix="AUTOTEST_"))
    organization: str | None = None


class SessionAction(SessionActionInput):
    id: int
