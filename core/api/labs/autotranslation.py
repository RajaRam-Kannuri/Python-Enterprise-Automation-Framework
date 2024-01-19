from core.api.base_refactored.api_client import ManagerApiClient, SingleItemApiClient
from core.api.base_refactored.api_wrapper import GettableWrapper
from core.api.labs.base import LabsCommonManager
from core.models.labs.translations import AutoTranslation, AutoTranslationInput
from settings import settings


class AutoTranslationClient(SingleItemApiClient):
    URL_TEMPLATE = f"{settings.base_url_labs}api/auto-translations/{{id}}/"
    NAME = "lab content auto-translation"


class AutoTranslationWrapper(GettableWrapper[AutoTranslationClient, AutoTranslation]):
    API_CLASS = AutoTranslationClient
    DATA_MODEL = AutoTranslation

    @property
    def is_finalized(self) -> bool:
        return False


class AutoTranslationsManagerClient(ManagerApiClient):
    URL = f"{settings.base_url_labs}api/auto-translations/"


class AutoTranslationsManager(
    LabsCommonManager[AutoTranslationsManagerClient, AutoTranslationWrapper, AutoTranslationInput]
):
    API_CLASS = AutoTranslationsManagerClient
    SINGLE_OBJECT_CLASS = AutoTranslationWrapper
    CREATE_MODEL = AutoTranslationInput
