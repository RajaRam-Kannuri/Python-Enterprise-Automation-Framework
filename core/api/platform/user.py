from http import HTTPStatus

import allure
from pydantic import parse_raw_as
from requests import Response

from core.api.base_api import ObjectCreatableApi, ObjectQueryableApi, ObjectUpdateableApi
from core.api.platform.base import PlatformGettableApi
from core.models.platform.base import PlatformListModel
from core.models.platform.platform_user import CreatePlatformUser, PlatformUser, UpdatePlatformUser
from core.models.platform.role import RoleAssignedToUser
from settings import settings
from util.assertions.common_assertions import assert_response_status


class UsersApi(
    PlatformGettableApi[PlatformUser],
    ObjectQueryableApi[PlatformUser],
    ObjectCreatableApi[CreatePlatformUser, PlatformUser],
    ObjectUpdateableApi[UpdatePlatformUser, PlatformUser],
):
    NAME = "Users"
    PATH_NAME = "users"
    URL = f"{settings.base_url_platform_api}{PATH_NAME}"
    MODEL = PlatformUser

    def get_current_user(self) -> PlatformUser:
        with allure.step("Get current user info"):
            return self.get("me")

    def request_user_roles(self, obj_id: str) -> Response:
        return self.session.get(f"{self.get_instance_url(obj_id)}/roles")

    def get_user_roles(self, obj_id: str) -> PlatformListModel[RoleAssignedToUser]:
        with allure.step("Get user roles"):
            response = self.request_user_roles(obj_id)
            assert_response_status(response.status_code, HTTPStatus.OK)
            return parse_raw_as(PlatformListModel[RoleAssignedToUser], response.text)
