import allure
import requests

from core.api.base_refactored.api_client import ManagerApiClient, SingleItemApiClient
from core.api.base_refactored.api_wrapper import GettableWrapper, QueryablesManager
from core.models.labs.translations import BackendsTranslation, Translation
from settings import settings


class BackendsTranslationClient(SingleItemApiClient):
    URL_TEMPLATE = f"{settings.base_url_labs}api/translation-backends/{{id}}/"
    NAME = "backend translation"


class BackendsTranslationWrapper(GettableWrapper[BackendsTranslationClient, BackendsTranslation]):
    API_CLASS = BackendsTranslationClient
    DATA_MODEL = BackendsTranslation

    @property
    def is_finalized(self) -> bool:
        return False


class BackendsTranslationsManagerClient(ManagerApiClient):
    URL = f"{settings.base_url_labs}api/translation-backends/"


class BackendsTranslationsManager(QueryablesManager[BackendsTranslationsManagerClient, BackendsTranslationWrapper]):
    API_CLASS = BackendsTranslationsManagerClient
    SINGLE_OBJECT_CLASS = BackendsTranslationWrapper


class TranslationClient(SingleItemApiClient):
    URL_TEMPLATE = f"{settings.base_url_labs}api/translations/{{id}}/"
    NAME = "translation"

    def request_approve(self) -> requests.Response:
        with allure.step(f"Approve translation for {self}"):
            response = self.api_session.patch(url=f"{self.url}approve/")
            return response


class TranslationWrapper(GettableWrapper[TranslationClient, Translation]):
    API_CLASS = TranslationClient
    DATA_MODEL = Translation

    @property
    def is_finalized(self) -> bool:
        return False


class TranslationsManagerClient(ManagerApiClient):
    URL = f"{settings.base_url_labs}api/translations/"


class TranslationsManager(QueryablesManager[TranslationsManagerClient, TranslationWrapper]):
    API_CLASS = TranslationsManagerClient
    SINGLE_OBJECT_CLASS = TranslationWrapper
