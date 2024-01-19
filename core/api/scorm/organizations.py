from http import HTTPStatus
from pathlib import Path

import allure
from requests import Response

from core.api.base import ApiObject, ApiObjectManager
from core.api.base_api import ObjectApi
from core.models.lms.lms_base import LMSModelBase
from core.models.scorm.organization import Organization as OrganizationModel
from core.models.scorm.organization import UpdateOrganization
from settings import settings
from util.assertions.common_assertions import assert_response_status


class OrganizationsApi(ObjectApi):
    NAME = "Organization"
    PATH_NAME = "organizations"
    URL = f"{settings.base_url_scorm_api}{PATH_NAME}"
    MODEL = OrganizationModel

    def request_post_file(self, resource_launch_id: str, file_path: Path) -> Response:
        with file_path.open("rb") as file:
            return self.session.post(self.URL, files={"file": file}, params={"resourceLaunchId": resource_launch_id})

    def post_file(self, resource_launch_id: str, file_path: Path) -> OrganizationModel:
        if not file_path.exists():
            raise RuntimeError(f"File {file_path} does not exist")

        with allure.step(f"Create {self.NAME} from {file_path}"):
            response = self.request_post_file(resource_launch_id, file_path)
            assert_response_status(response.status_code, HTTPStatus.OK)

            return OrganizationModel.parse_raw(response.text)

    def request_get(self, resource_launch_id: str, obj_id: str) -> Response:
        return self.session.get(self.get_instance_url(obj_id), params={"resourceLaunchId": resource_launch_id})

    def get(self, resource_launch_id: str, obj_id: str) -> OrganizationModel:
        with allure.step(f"Get {self.NAME} with ID {obj_id} using launch ID {resource_launch_id}"):
            response = self.request_get(resource_launch_id, obj_id)
            assert_response_status(response.status_code, HTTPStatus.OK)

            return OrganizationModel.parse_raw(response.text)

    def put(self, resource_launch_id: str, obj_id: str, update_data: UpdateOrganization) -> OrganizationModel:
        with allure.step(f"Update {self.NAME} with ID {obj_id} using launch ID {resource_launch_id}"):
            response = self.request_put(resource_launch_id, obj_id, update_data)
            assert_response_status(response.status_code, HTTPStatus.OK)

            return OrganizationModel.parse_raw(response.text)

    def request_put(self, resource_launch_id: str, obj_id: str, payload: LMSModelBase | dict) -> Response:
        data = payload.lms_dict() if isinstance(payload, LMSModelBase) else payload
        return self.session.put(
            self.get_instance_url(obj_id), json=data, params={"resourceLaunchId": resource_launch_id}
        )


class Organization(ApiObject[OrganizationModel, OrganizationsApi]):
    API = OrganizationsApi

    def update(self, resource_launch_id: str, **non_default_params):
        with allure.step(f"Update Organization with ID {self.data.id} using launch ID {resource_launch_id}"):
            default_params = {
                "title": self.data.title,
                "version": self.data.version,
                "code": self.data.code,
                "state": self.data.state,
            }

            update_params = {**default_params, **non_default_params}
            update_data = UpdateOrganization(**update_params)

            return self._api.put(resource_launch_id, self.data.id, update_data)


class OrganizationManager(ApiObjectManager[OrganizationsApi, Organization]):
    API = OrganizationsApi
    OBJECT = Organization

    def create_from_file(self, resource_launch_id: str, file_path: Path) -> Organization:
        with allure.step(f"Create Organization from file {file_path}"):
            api_result = self._api.post_file(resource_launch_id, file_path)
            return self.OBJECT(self.session, api_result)

    def get(self, resource_launch_id: str, obj_id: str) -> Organization:
        with allure.step(f"Get Organization with ID {obj_id} using launch ID {resource_launch_id}"):
            api_result = self._api.get(resource_launch_id, obj_id)
            return self.OBJECT(self.session, api_result)
