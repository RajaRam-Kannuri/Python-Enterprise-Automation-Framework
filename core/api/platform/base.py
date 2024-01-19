from http import HTTPStatus
from typing import Generic

from pydantic import parse_raw_as

from core.api.base_api import ApiModel, ObjectGettableApi
from core.models.platform.base import PlatformListModel
from util.assertions.common_assertions import assert_response_status


class PlatformGettableApi(ObjectGettableApi[ApiModel], Generic[ApiModel]):
    def list(self) -> PlatformListModel[ApiModel]:
        response = self.request_list()
        assert_response_status(response.status_code, HTTPStatus.OK)
        return parse_raw_as(PlatformListModel[self.MODEL], response.text)
