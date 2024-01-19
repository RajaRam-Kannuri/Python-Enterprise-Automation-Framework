from enum import StrEnum

from pydantic import BaseModel, validator


class BaseUser(BaseModel):
    email: str
    password: str


# From platform seeds:
# https://gitlab.constr.dev/platform/aps/platform-api/-/blob/main/resources/seeds/data.yaml#L1335
class TestRoles(StrEnum):
    ADMIN = "Administrator"
    AUTHOR = "Author"
    INSTRUCTOR = "Instructor"
    LEARNER = "Learner"
    PROCTOR = "Proctor"


class TeamRoles(StrEnum):
    LEAD = "Lead"
    CONTRIBUTOR = "Contributor"
    REVIEWER = "Reviewer"

    def get_name(self, team_name: str) -> str:
        return f"Team{self}_{team_name}"


class User(BaseUser):
    username: str | None
    roles: set[TestRoles] = set()
    team_roles: set[TeamRoles] = set()

    @validator("username", always=True, pre=True)
    def validate_username(cls, v, values):
        if not v:
            v = values["email"]
        return v


class LabsUser(BaseUser):
    organization_name: str | None = None
