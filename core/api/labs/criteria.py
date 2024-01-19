from core.api.base_refactored.api_client import ManagerApiClient, SingleItemApiClient
from core.api.labs.base import LabsCommonManager, LabsCommonObjectWrapper
from core.models.labs.step_criteria import StepCriteria, StepCriteriaInput
from settings import settings


class CriteriaClient(SingleItemApiClient):
    NAME = "criteria"
    URL_TEMPLATE = f"{settings.base_url_labs}api/criterias/{{id}}/"


class CriteriaWrapper(LabsCommonObjectWrapper[CriteriaClient, StepCriteria, StepCriteriaInput]):
    API_CLASS = CriteriaClient
    DATA_MODEL = StepCriteria
    INPUT_CLASS_MODEL = StepCriteriaInput


class CriteriaManagerClient(ManagerApiClient):
    URL = f"{settings.base_url_labs}api/criterias/"


class CriteriaManager(LabsCommonManager[CriteriaManagerClient, CriteriaWrapper, StepCriteriaInput]):
    API_CLASS = CriteriaManagerClient
    SINGLE_OBJECT_CLASS = CriteriaWrapper
    CREATE_MODEL = StepCriteriaInput

    def create_session_action(self, input_data_model: StepCriteriaInput) -> CriteriaWrapper:
        return self.create(input_data_model)
