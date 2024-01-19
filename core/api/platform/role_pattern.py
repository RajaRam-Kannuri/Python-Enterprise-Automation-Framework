from http import HTTPStatus

import allure
from pydantic import parse_raw_as

from core.api.base_api import ObjectQueryableApi
from core.api.platform.base import PlatformGettableApi
from core.models.platform.base import PlatformListModel
from core.models.platform.role_pattern import RolePattern, RolePatternPermission
from settings import settings
from util.assertions.common_assertions import assert_response_status


class RolePatternsApi(
    PlatformGettableApi[RolePattern],
    ObjectQueryableApi[RolePattern],
):
    NAME = "Role patterns"
    PATH_NAME = "role-patterns"
    URL = f"{settings.base_url_platform_api}{PATH_NAME}"
    MODEL = RolePattern

    def get_role_pattern_permissions(
        self,
        obj_id: str,
        app_id: str | None = None,
        offset: int | None = None,
        limit: int | None = None,
    ) -> PlatformListModel[RolePatternPermission]:
        params = {}
        if app_id is not None:
            params["app_filter"] = app_id
        if offset is not None:
            params["offset"] = offset
        if limit is not None:
            params["limit"] = limit

        with allure.step("Get role pattern permissions"):
            response = self.session.get(f"{self.get_instance_url(obj_id)}/role-pattern-permissions", params=params)
            assert_response_status(response.status_code, HTTPStatus.OK)
            return parse_raw_as(PlatformListModel[RolePatternPermission], response.text)
