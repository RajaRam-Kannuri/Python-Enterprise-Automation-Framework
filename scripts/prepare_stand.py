import logging

from requests import Session

from core.api.auth import authorize_platform_user
from core.api.base_api import ObjectNotFound
from core.api.platform.roles import RolesApi
from core.api.platform.team import TeamsApi
from core.api.platform.user import UsersApi
from core.api.platform.user_roles import UserRolesApi
from core.models.platform.platform_user import CreatePlatformUser, PlatformUser
from core.models.platform.team import CreateTeam, Team
from core.models.platform.user_role import CreateUserRole
from core.models.query import LoadOptions
from core.models.user import TeamRoles, TestRoles, User
from test_data.stand_config import StandConfig

logger = logging.getLogger("prepare_stand")


def get_or_create_team(session: Session, team_id: str) -> Team:
    teams_api = TeamsApi(session=session)
    try:
        team = teams_api.get(team_id)
        logger.info(f"Team '{team.name}' already exists")
    except ObjectNotFound:
        logger.info(f"Team {team_id} does not exist, creating")
        team = teams_api.post(CreateTeam(id=team_id, name="Autotest Team", description="Team for automated testing"))
    return team


def get_or_create_platform_user(session: Session, user: User) -> PlatformUser:
    users_api = UsersApi(session=session)

    query_result = users_api.query(LoadOptions(take=1, filter=f'["email","=","{user.email}"]'))

    if len(query_result.data) > 0:
        logger.info(f"User '{user.email}' already exists")
        user = query_result.data[0]
    else:
        logger.info(f"User '{user.email}' does not exist, creating")
        user = users_api.post(
            CreatePlatformUser(
                email=user.email,
                username=user.email,
                password=user.password,
            )
        )
    return user


def set_user_roles(
    session: Session, platform_user: PlatformUser, roles: set[TestRoles], team_roles: set[TeamRoles], team: Team
) -> None:
    users_api = UsersApi(session=session)
    roles_api = RolesApi(session=session)
    user_roles_api = UserRolesApi(session=session)

    logger.info(f"Check roles for user '{platform_user.email}'")
    platform_roles = {rli.name: rli for rli in roles_api.list().items}
    current_user_roles = {rli.role.name: rli.role for rli in users_api.get_user_roles(platform_user.id).items}
    for role_name in roles:
        if role_name not in current_user_roles:
            logger.info(f"Role '{role_name}' is not set for user '{platform_user.email}', creating")
            role = platform_roles[role_name]
            user_roles_api.post(CreateUserRole(user_id=platform_user.id, role_id=role.id))

    for team_role_pattern in team_roles:
        role_name = team_role_pattern.get_name(team.name)
        if role_name not in current_user_roles:
            logger.info(f"Role '{role_name}' is not set for user '{platform_user.email}', creating")
            role = platform_roles[role_name]
            user_roles_api.post(CreateUserRole(user_id=platform_user.id, role_id=role.id))


def prepare_stand(config: StandConfig):
    session = Session()

    all_roles_user = config.platform_users["all_roles"]
    authorize_platform_user(session=session, user=all_roles_user)

    team = get_or_create_team(session=session, team_id=config.team_id)

    for user_key, user in config.platform_users.items():
        platform_user = get_or_create_platform_user(session, user)
        set_user_roles(
            session=session, platform_user=platform_user, roles=user.roles, team_roles=user.team_roles, team=team
        )


if __name__ == "__main__":
    from settings import Environment, settings

    if settings.stand == Environment.PRODUCTION:
        raise RuntimeError("Running stand preparation in production is not supported")

    logging.basicConfig(level=logging.INFO)

    logger.info(f"Start {settings.stand} stand preparation")
    prepare_stand(settings.stand_config)
    logger.info("Stand preparation finished")
