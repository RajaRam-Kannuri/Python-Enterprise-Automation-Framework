import allure
import requests

from core.api.base_refactored.api_client import ManagerApiClient, SingleItemApiClient
from core.api.base_refactored.api_wrapper import SelfStateChangingWrapper
from core.api.labs.base import LabsCommonManager, LabsCommonObjectWrapper
from core.api.labs.image import ImageWrapper
from core.models.labs.image import ExternalImageInput
from core.models.labs.vm import ExternalVM, ExternalVMInput, VMStatuses
from settings import settings


class VmClient(SingleItemApiClient):
    NAME = "image"
    URL_TEMPLATE = f"{settings.base_url_labs}api/vms/{{id}}/"

    def request_save(self, payload: dict) -> requests.Response:
        with allure.step(f'saving {self} as image with data "{payload}"'):
            response = self.api_session.post(url=f"{self.url}save/", json=payload)
            return response


class VmWrapper(
    LabsCommonObjectWrapper[VmClient, ExternalVM, ExternalVMInput], SelfStateChangingWrapper[VmClient, ExternalVM]
):
    API_CLASS = VmClient
    DATA_MODEL = ExternalVM
    INPUT_CLASS_MODEL = ExternalVMInput

    @property
    def states(self):
        return VMStatuses

    def wait_for_state(self, desired_state: VMStatuses, timeout=settings.image_preparation_timeout):
        super().wait_for_state(desired_state=desired_state, timeout=timeout)

    def save_as_image(self, image: ExternalImageInput) -> ImageWrapper:
        image_dict = image.dict(exclude_none=True)
        response = self.api.request_save(image_dict)
        response.raise_for_status()
        image = ImageWrapper(self.api_session, data=response.json())
        return image


class VmsManagerClient(ManagerApiClient):
    URL = f"{settings.base_url_labs}api/vms/"


class VmsManager(LabsCommonManager[VmsManagerClient, VmWrapper, ExternalVMInput]):
    API_CLASS = VmsManagerClient
    SINGLE_OBJECT_CLASS = VmWrapper
    CREATE_MODEL = ExternalVMInput

    def create_vm(self, image_id: str) -> VmWrapper:
        return self.create(ExternalVMInput(image_id=image_id))
