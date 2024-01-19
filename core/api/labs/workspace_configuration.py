from typing import Self

import allure
import requests

from core.api.base_refactored.api_client import ManagerApiClient, SingleItemApiClient
from core.api.labs.base import LabsCommonManager, LabsCommonObjectWrapper
from core.models.labs.workspace_configuration import WorkspaceConfiguration, WorkspaceConfigurationInput
from settings import settings


class WorkspaceConfigClient(SingleItemApiClient):
    NAME = "workspace configuration"
    URL_TEMPLATE = f"{settings.base_url_labs}api/workspace/configuration/{{id}}/"

    def request_copy(self) -> requests.Response:
        with allure.step(f'copying {self} "'):
            response = self.api_session.post(url=f"{self.url}copy/")
            return response


class WorkspaceConfigWrapper(
    LabsCommonObjectWrapper[WorkspaceConfigClient, WorkspaceConfiguration, WorkspaceConfigurationInput]
):
    API_CLASS = WorkspaceConfigClient
    DATA_MODEL = WorkspaceConfiguration
    INPUT_CLASS_MODEL = WorkspaceConfigurationInput

    def copy(self) -> Self:
        response = self.api.request_copy()
        response.raise_for_status()
        return WorkspaceConfigWrapper(api_session=self.api_session, data=response.json())


class WorkspaceConfigsManagerClient(ManagerApiClient):
    URL = f"{settings.base_url_labs}api/workspace/configuration/"

    def request_check_unique(self, payload: dict) -> requests.Response:
        """returns true/false"""
        with allure.step(f'checking if workspace configuration with data "{payload}" is unique'):
            response = self.api_session.get(
                url=f"{settings.base_url_labs}api/workspace/configuration-check-unique/", params=payload
            )
            return response


class WorkspaceConfigurationsManager(
    LabsCommonManager[WorkspaceConfigsManagerClient, WorkspaceConfigWrapper, WorkspaceConfigurationInput]
):
    API_CLASS = WorkspaceConfigsManagerClient
    SINGLE_OBJECT_CLASS = WorkspaceConfigWrapper
    CREATE_MODEL = WorkspaceConfigurationInput

    def create_workspace_configuration(
        self, input_data_model: WorkspaceConfigurationInput = None
    ) -> WorkspaceConfigWrapper:
        return self.create(input_data_model or WorkspaceConfigurationInput())

    def response_check_unique(self, payload: dict) -> bool:
        response = self.api.request_check_unique(payload)
        response.raise_for_status()
        return response.json()["is_unique"]
