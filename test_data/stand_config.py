from pathlib import Path

from pydantic import BaseSettings

from core.models.user import LabsUser, TeamRoles, TestRoles, User
from test_data.users import CUSTOM_DOMAIN_USERS, DEFAULT_DOMAIN_USERS, DEFAULT_LABS_USERS, DEFAULT_PASSWORD, PROD_USERS

PROJECT_ROOT = Path(__file__).parent.parent.absolute()


class StandConfig(BaseSettings):
    tenant_id: str
    team_id: str
    platform_users: dict[str, User]
    labs_users: dict[str, LabsUser]

    @property
    def users(self) -> dict[str, User | LabsUser]:
        return {
            **self.platform_users,
            **self.labs_users,
        }


# https://gitlab.constr.dev/platform/aps/platform-api/-/blob/main/resources/seeds/data.yaml#L713
DEFAULT_TENANT_ID = "39e7fbd8-c4f3-456a-a744-dd43862ba8d3"

# https://gitlab.constr.dev/platform/alms/core/-/blob/master/Utils/Migrate/Seeders/Constants.cs#L24
DEFAULT_TEAM_ID = "6a4b326f-bf90-4dbd-84ee-2518955600d3"


STAGE_CONFIG = StandConfig(
    tenant_id=DEFAULT_TENANT_ID,
    team_id=DEFAULT_TEAM_ID,
    platform_users=DEFAULT_DOMAIN_USERS,
    labs_users=DEFAULT_LABS_USERS,
)
TEST_CONFIG = StandConfig(
    tenant_id=DEFAULT_TENANT_ID,
    team_id=DEFAULT_TEAM_ID,
    platform_users=DEFAULT_DOMAIN_USERS,
    labs_users=DEFAULT_LABS_USERS,
)
DEV_CONFIG = StandConfig(
    tenant_id=DEFAULT_TENANT_ID,
    team_id=DEFAULT_TEAM_ID,
    platform_users=DEFAULT_DOMAIN_USERS,
    labs_users=DEFAULT_LABS_USERS,
)

PROD_CONFIG = StandConfig(
    tenant_id=DEFAULT_TENANT_ID,
    team_id=DEFAULT_TEAM_ID,
    platform_users=PROD_USERS,
    labs_users={},
)

CUSTOM_DOMAIN_STAGE_CONFIG = StandConfig(
    tenant_id="d9be9e88-cdb6-4d17-81d4-f4199c574cde",
    team_id="1330fe99-94ff-4a13-b323-18519f2f4128",
    platform_users={
        "all_roles": User(
            email="admin@dummy-tenant.com",
            password=DEFAULT_PASSWORD,
            roles={TestRoles.ADMIN, TestRoles.LEARNER, TestRoles.INSTRUCTOR, TestRoles.AUTHOR},
        ),
        **CUSTOM_DOMAIN_USERS,
    },
    labs_users=DEFAULT_LABS_USERS,
)

CUSTOM_DOMAIN_TEST_CONFIG = StandConfig(
    tenant_id="af0e4e0e-8444-4578-a0c6-b8a797158275",
    team_id="1330fe99-94ff-4a13-b323-18519f2f4128",
    platform_users={
        "all_roles": User(
            email="3rdpartyadmintest@company.com",
            password=DEFAULT_PASSWORD,
            roles={TestRoles.ADMIN, TestRoles.LEARNER, TestRoles.INSTRUCTOR, TestRoles.AUTHOR},
            team_roles={TeamRoles.LEAD, TeamRoles.CONTRIBUTOR, TeamRoles.REVIEWER},
        ),
        **CUSTOM_DOMAIN_USERS,
    },
    labs_users=DEFAULT_LABS_USERS,
)

CUSTOM_DOMAIN_DEV_CONFIG = StandConfig(
    tenant_id="5169ddae-f956-4d98-bc04-0a8683619c89",
    team_id="1330fe99-94ff-4a13-b323-18519f2f4128",
    platform_users={
        "all_roles": User(
            email="admin@dummy-tenant.com",
            password=DEFAULT_PASSWORD,
            roles={TestRoles.ADMIN, TestRoles.LEARNER, TestRoles.INSTRUCTOR, TestRoles.AUTHOR},
            team_roles={TeamRoles.LEAD, TeamRoles.CONTRIBUTOR, TeamRoles.REVIEWER},
        ),
        **CUSTOM_DOMAIN_USERS,
    },
    labs_users=DEFAULT_LABS_USERS,
)
