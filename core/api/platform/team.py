from http import HTTPStatus

from pydantic import parse_raw_as
from requests import Response

from core.api.base_api import ObjectCreatableApi, ObjectDeleteableApi, ObjectQueryableApi, ObjectUpdateableApi
from core.api.platform.base import PlatformGettableApi
from core.models.platform.base import PlatformListModel
from core.models.platform.platform_user import UserWithUserRoleId
from core.models.platform.role import Role
from core.models.platform.team import CreateTeam, Team, UpdateTeam
from settings import settings
from util.assertions.common_assertions import assert_response_status


class TeamsApi(
    PlatformGettableApi[Team],
    ObjectQueryableApi[Team],
    ObjectCreatableApi[CreateTeam, Team],
    ObjectUpdateableApi[UpdateTeam, Team],
    ObjectDeleteableApi,
):
    NAME = "Teams"
    PATH_NAME = "teams"
    URL = f"{settings.base_url_platform_api}{PATH_NAME}"
    MODEL = Team

    def request_get_users(self, obj_id: str) -> Response:
        return self.session.get(f"{self.get_instance_url(obj_id)}/user-roles")

    def get_team_users(self, obj_id: str) -> PlatformListModel[UserWithUserRoleId]:
        response = self.request_get_users(obj_id)
        assert_response_status(response.status_code, HTTPStatus.OK)

        return parse_raw_as(PlatformListModel[UserWithUserRoleId], response.text)

    def requeste_get_roles(self, obj_id: str) -> Response:
        return self.session.get(f"{self.get_instance_url(obj_id)}/roles")

    def get_team_roles(self, obj_id: str) -> PlatformListModel[Role]:
        response = self.requeste_get_roles(obj_id)
        assert_response_status(response.status_code, HTTPStatus.OK)

        return parse_raw_as(PlatformListModel[Role], response.text)
