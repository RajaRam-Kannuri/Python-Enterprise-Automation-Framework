from http import HTTPStatus

from pydantic import parse_raw_as
from requests import Response

from core.api.base_api import ObjectCreatableApi, ObjectQueryableApi, ObjectUpdateableApi, check_response
from core.api.platform.base import PlatformGettableApi
from core.models.platform.base import PlatformListModel
from core.models.platform.group import CreateGroup, Group, UpdateGroup, UserMembershipInGroup, UserWithGroupMembership
from settings import settings


class GroupsApi(
    PlatformGettableApi[Group],
    ObjectQueryableApi[Group],
    ObjectCreatableApi[CreateGroup, Group],
    ObjectUpdateableApi[UpdateGroup, Group],
):
    NAME = "Group"
    PATH_NAME = "groups"
    URL = f"{settings.base_url_platform_api}{PATH_NAME}"
    MODEL = Group

    def request_add_user(self, obj_id: str, user_id: str) -> Response:
        return self.session.post(f"{self.get_instance_url(obj_id)}/users/{user_id}", json={})

    def add_user(self, obj_id: str, user_id: str):
        response = self.request_add_user(obj_id, user_id)
        check_response(response, HTTPStatus.OK)

    def request_get_users(self, obj_id: str) -> Response:
        return self.session.get(f"{self.get_instance_url(obj_id)}/users")

    def get_users(self, obj_id: str) -> PlatformListModel[UserWithGroupMembership]:
        response = self.request_get_users(obj_id)
        check_response(response, HTTPStatus.OK)

        return parse_raw_as(PlatformListModel[UserWithGroupMembership], response.text)

    def request_get_user(self, obj_id: str, user_id: str) -> Response:
        return self.session.get(f"{self.get_instance_url(obj_id)}/users/{user_id}")

    def get_user(self, obj_id: str, user_id: str) -> PlatformListModel[UserMembershipInGroup]:
        response = self.request_get_user(obj_id, user_id)
        check_response(response, HTTPStatus.OK)

        return parse_raw_as(PlatformListModel[UserMembershipInGroup], response.text)

    def request_delete_user(self, obj_id: str, user_id: str) -> Response:
        return self.session.delete(f"{self.get_instance_url(obj_id)}/users/{user_id}", json={})

    def delete_user(self, obj_id: str, user_id: str) -> None:
        response = self.request_delete_user(obj_id, user_id)
        check_response(response, HTTPStatus.NO_CONTENT)
