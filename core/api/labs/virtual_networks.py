from typing import Union

import allure

from core.api.base_refactored.api_client import ManagerApiClient
from core.api.base_refactored.api_wrapper import GettableWrapper, QueryablesManager
from core.models.labs.virtual_network import ExternalImageProvider, Network, NetworkInput, SupportedNetworks
from settings import settings


class VirtualNetworksManagerClient(ManagerApiClient):
    URL = f"{settings.base_url}/api/labs/providers/{ExternalImageProvider.GCE.value}/available-virtual-networks/"


class VirtualNetworksWrapper(GettableWrapper[VirtualNetworksManagerClient, Network]):
    API_CLASS = None
    DATA_MODEL = Network
    INPUT_CLASS_MODEL = NetworkInput

    @property
    def is_finalized(self) -> bool:
        return False


class VirtualNetworksManager(QueryablesManager[VirtualNetworksManagerClient, VirtualNetworksWrapper]):
    API_CLASS = VirtualNetworksManagerClient
    SINGLE_OBJECT_CLASS = VirtualNetworksWrapper

    def get_network_id(self, name: Union[SupportedNetworks, str] = SupportedNetworks.PUBLIC):
        with allure.step(f'Find network that matches "{name}" from list of images'):
            # networks can be None for tenants because they need quotas which take a lot of resources, and added
            # separately for each tenant

            network_list = [
                item["id"]
                for item in self.api.request_query({"firewall_rules_type": name}).json()
                if item["firewall_rules_type"] == name
            ]
            virtual_network_id = network_list[0] if network_list else None
            return virtual_network_id
