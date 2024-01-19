from core.api.base_refactored.api_client import ManagerApiClient, SingleItemApiClient
from core.api.base_refactored.api_wrapper import GettableWrapper
from core.api.labs.base import LabsCommonManager
from core.models.labs.language import LabLanguage, LabLanguageInput
from settings import settings


class LanguageClient(SingleItemApiClient):
    URL_TEMPLATE = f"{settings.base_url_labs}api/languages/{{id}}/"
    NAME = "lab language"


class LanguageWrapper(GettableWrapper[LanguageClient, LabLanguage]):
    API_CLASS = LanguageClient
    DATA_MODEL = LabLanguage

    @property
    def is_finalized(self) -> bool:
        return False


class LanguagesManagerClient(ManagerApiClient):
    URL = f"{settings.base_url_labs}api/languages/"


class LanguagesManager(LabsCommonManager[LanguagesManagerClient, LanguageWrapper, LabLanguageInput]):
    API_CLASS = LanguagesManagerClient
    SINGLE_OBJECT_CLASS = LanguageWrapper
    CREATE_MODEL = LabLanguageInput
