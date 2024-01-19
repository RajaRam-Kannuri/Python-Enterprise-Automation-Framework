from http import HTTPStatus

import allure
from pydantic import parse_raw_as

from core.api.base_api import ObjectCreatableApi, ObjectDeleteableApi, ObjectQueryableApi, ObjectUpdateableApi
from core.api.platform.base import PlatformGettableApi
from core.models.platform.base import PlatformListModel
from core.models.platform.permission import PermissionAssignedToRole
from core.models.platform.role import CreateRole, Role, UpdateRole
from settings import settings
from util.assertions.common_assertions import assert_response_status


class RolesApi(
    PlatformGettableApi[Role],
    ObjectQueryableApi[Role],
    ObjectCreatableApi[CreateRole, Role],
    ObjectUpdateableApi[UpdateRole, Role],
    ObjectDeleteableApi,
):
    NAME = "Roles"
    PATH_NAME = "roles"
    URL = f"{settings.base_url_platform_api}{PATH_NAME}"
    MODEL = Role

    def get_role_permissions(
        self,
        obj_id: str,
        app_id: str | None = None,
        offset: int | None = None,
        limit: int | None = None,
    ) -> PlatformListModel[PermissionAssignedToRole]:
        params = {}
        if app_id is not None:
            params["app_filter"] = app_id
        if offset is not None:
            params["offset"] = offset
        if limit is not None:
            params["limit"] = limit

        with allure.step("Get role permissions"):
            response = self.session.get(f"{self.get_instance_url(obj_id)}/permissions", params=params)
            assert_response_status(response.status_code, HTTPStatus.OK)
            return parse_raw_as(PlatformListModel[PermissionAssignedToRole], response.text)
