import allure
import requests
from waiting import wait

from core.api.base_refactored.api_client import ManagerApiClient, SingleItemApiClient
from core.api.base_refactored.api_wrapper import QueryablesManager
from core.api.labs.base import LabsCommonObjectWrapper
from core.models.labs.image import ExternalImage, ExternalImageInput
from settings import settings


class ImageClient(SingleItemApiClient):
    NAME = "image"
    URL_TEMPLATE = f"{settings.base_url_labs}api/images/{{id}}/"


class ImageWrapper(LabsCommonObjectWrapper[ImageClient, ExternalImage, ExternalImageInput]):
    API_CLASS = ImageClient
    DATA_MODEL = ExternalImage
    INPUT_CLASS_MODEL = ExternalImageInput
    DEFAULT_TEARDOWN_TIMEOUT = settings.image_preparation_timeout

    def __repr__(self):
        return f'{self.API_CLASS.NAME} "{self.name}" (id={self.id})'

    def wait_until_be_ready(self, timeout=settings.image_preparation_timeout) -> requests.Response:
        """
        Wait until the image is ready
        """

        def poll_get_image():
            res = self.api.request_get()
            return res if res.json()["is_ready"] else None

        with allure.step(f"Waiting until {self} will be ready"):
            response = wait(
                poll_get_image,
                waiting_for=f"until {self} will be ready",
                timeout_seconds=timeout,
            )
        self._update_inner_data(response)
        return response


class ImagesManagerClient(ManagerApiClient):
    URL = f"{settings.base_url_labs}api/images/"


class ImagesManager(QueryablesManager[ImagesManagerClient, ImageWrapper]):
    API_CLASS = ImagesManagerClient
    SINGLE_OBJECT_CLASS = ImageWrapper
