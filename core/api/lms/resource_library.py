from http import HTTPStatus

import allure
from pydantic import parse_raw_as
from requests import Response

from core.api.lms.base import LMSApiObject, LMSApiObjectManager
from core.api.lms.base_api import LmsAsyncApi
from core.models.lms.resource_library import CreateResourceLibrary, Resource
from core.models.lms.resource_library import ResourceLibrary as ResourceLibraryModel
from core.models.lms.resource_library import ResourceLibraryAction, ResourceLibraryType, UpdateResourceLibrary
from core.models.lti.lti_resource_library import LtiResourceInitModel
from core.models.query import LoadOptions
from settings import settings
from util.assertions.common_assertions import assert_response_status
from util.helpers import first


class ResourceLibraryApi(LmsAsyncApi[ResourceLibraryModel, CreateResourceLibrary, UpdateResourceLibrary]):
    NAME = "Resource Library"
    PATH_NAME = "resource-libraries"
    URL = f"{settings.base_url_lms_api}{PATH_NAME}"
    MODEL = ResourceLibraryModel

    def request_get_actions(self, obj_id: str) -> Response:
        return self.session.get(f"{self.get_instance_url(obj_id)}/actions")

    def get_actions(self, obj_id: str) -> list[ResourceLibraryAction]:
        with allure.step(f"Get actions for {obj_id} resource library"):
            response = self.request_get_actions(obj_id)
            assert_response_status(response.status_code, HTTPStatus.OK)
            return parse_raw_as(list[ResourceLibraryAction], response.text)

    def request_get_resources(self, obj_id: str) -> Response:
        return self.session.get(f"{self.get_instance_url(obj_id)}/resources")

    def get_resources(self, obj_id: str) -> list[Resource]:
        with allure.step(f"Get resources for {obj_id} resource library"):
            response = self.request_get_resources(obj_id)
            assert_response_status(response.status_code, HTTPStatus.OK)

            return parse_raw_as(list[Resource], response.text)

    def request_get_resource(self, obj_id: str, resource_path: str):
        return self.session.get(f"{self.get_instance_url(obj_id)}/resources/{resource_path}")

    def get_resource(self, obj_id: str, resource_path: str) -> list[Resource]:
        with allure.step(f"Get resource with id {resource_path} for {obj_id} resource library"):
            response = self.request_get_resource(obj_id, resource_path)
            assert_response_status(response.status_code, HTTPStatus.OK)

            return parse_raw_as(list[Resource], response.text)

    def request_get_lti_form(self, obj_id: str):
        return self.session.get(f"{settings.base_url_lms_api}lti-resource-libraries/{obj_id}/lti-form")

    def get_lti_form(self, obj_id: str) -> LtiResourceInitModel:
        with allure.step(f"Get lti form for library {obj_id}"):
            response = self.request_get_lti_form(obj_id)
            assert_response_status(response.status_code, HTTPStatus.OK)

            return LtiResourceInitModel.parse_raw(response.text)


class ResourceLibrary(LMSApiObject[ResourceLibraryModel, ResourceLibraryApi]):
    API = ResourceLibraryApi

    @property
    def actions(self) -> list[ResourceLibraryAction]:
        with allure.step(f"Get actions for resource library {self.id}"):
            return self._api.get_actions(self.id)

    @property
    def resources(self) -> list[Resource]:
        with allure.step(f"Get resources for resource library {self.id}"):
            return self._api.get_resources(self.id)

    def get_resource(self, resource_path: str) -> list[Resource]:
        with allure.step(f"Get resource {resource_path} for resource library {self.id}"):
            return self._api.get_resource(self.id, resource_path)

    @property
    def lti_form(self) -> LtiResourceInitModel:
        with allure.step(f"Get lti form for resource library {self.id}"):
            return self._api.get_lti_form(self.id)


class ResourceLibraryManager(LMSApiObjectManager[ResourceLibraryApi, ResourceLibrary]):
    API = ResourceLibraryApi
    OBJECT = ResourceLibrary

    def get_by_type(self, lib_type: ResourceLibraryType) -> ResourceLibrary | None:
        with allure.step(f"Get resource library with type: {lib_type}"):
            load_options = LoadOptions(take=1, filter=f'["type","=","{lib_type}"]')
            query_result = self.query(load_options)
            return first(query_result)

    def get_by_name(self, lib_name) -> ResourceLibrary | None:
        with allure.step(f"Get resource library name: {lib_name}"):
            load_options = LoadOptions(take=1, filter=f'["name","=","{lib_name}"]')
            query_result = self.query(load_options)
            return first(query_result)
