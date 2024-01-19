import requests

from core.api.base_refactored.api_client import DataPayload, ManagerApiClient, SingleItemApiClient, prepare_body
from core.api.labs.base import LabsCommonManager, LabsCommonObjectWrapper
from core.models.labs.workspace_configuration import (
    WorkspaceConfigurationItem,
    WorkspaceConfigurationItemInput,
    WorkspaceConfigurationItemUpdate,
)
from settings import settings


class WorkspaceConfigurationItemClient(SingleItemApiClient):
    NAME = "workspace configuration item"
    URL_TEMPLATE = f"{settings.base_url_labs}api/workspace/configuration-items/{{id}}/"


class WorkspaceConfigurationItemWrapper(
    LabsCommonObjectWrapper[
        WorkspaceConfigurationItemClient, WorkspaceConfigurationItem, WorkspaceConfigurationItemInput
    ]
):
    API_CLASS = WorkspaceConfigurationItemClient
    DATA_MODEL = WorkspaceConfigurationItem
    INPUT_CLASS_MODEL = WorkspaceConfigurationItemUpdate
    NAME_KEY_IN_PAYLOAD = "component_name"


class WorkspaceConfigurationsItemsClient(ManagerApiClient):
    URL = f"{settings.base_url_labs}api/workspace/configuration-items/"

    def request_post(self, create_data: DataPayload) -> requests.Response:
        # In case of virtual_network_id we cannot post None value - it returns 400 error. So we need to exclude this
        # field from payload if it is None.

        create_data = prepare_body(create_data)
        if "virtual_network_id" in create_data and create_data.get("virtual_network_id") is None:
            create_data.pop("virtual_network_id", None)
        return super().request_post(create_data)


class WorkspaceConfigurationItemsManager(
    LabsCommonManager[
        WorkspaceConfigurationsItemsClient, WorkspaceConfigurationItemWrapper, WorkspaceConfigurationItemInput
    ]
):
    API_CLASS = WorkspaceConfigurationsItemsClient
    CREATE_MODEL = WorkspaceConfigurationItemInput
    SINGLE_OBJECT_CLASS = WorkspaceConfigurationItemWrapper

    def create_workspace_configuration_item(
        self, input_data_model: WorkspaceConfigurationItemInput
    ) -> WorkspaceConfigurationItemWrapper:
        return self.create(input_data_model)
