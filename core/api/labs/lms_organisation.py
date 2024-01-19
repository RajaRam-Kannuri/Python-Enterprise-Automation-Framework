from core.api.base_refactored.api_client import ManagerApiClient, SingleItemApiClient
from core.api.base_refactored.api_wrapper import GettableWrapper, QueryablesManager
from core.models.labs.lms import LmsOrganisation, LmsOrganisationInput
from settings import settings


class LmsOrganisationClient(SingleItemApiClient):
    URL_TEMPLATE = f"{settings.base_url_labs}api/lms/{{id}}/"
    NAME = "lms organisation"


class LmsOrganisationWrapper(GettableWrapper[LmsOrganisationClient, LmsOrganisation]):
    API_CLASS = LmsOrganisationClient
    DATA_MODEL = LmsOrganisation
    INPUT_CLASS_MODEL = LmsOrganisationInput

    @property
    def is_finalized(self) -> bool:
        return False


class LmsOrganisationsManagerClient(ManagerApiClient):
    URL = f"{settings.base_url_labs}api/lms/"


class LmsOrganisationsManager(QueryablesManager[LmsOrganisationsManagerClient, LmsOrganisationWrapper]):
    API_CLASS = LmsOrganisationsManagerClient
    SINGLE_OBJECT_CLASS = LmsOrganisationWrapper
