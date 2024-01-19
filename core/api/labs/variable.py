from core.api.base_refactored.api_client import ManagerApiClient, SingleItemApiClient
from core.api.labs.base import LabsCommonManager, LabsCommonObjectWrapper
from core.models.labs.variable_template import VariableTemplate, VariableTemplateInput
from settings import settings


class TemplateVariableClient(SingleItemApiClient):
    NAME = "variable"
    URL_TEMPLATE = f"{settings.base_url_labs}api/labs/templatevariables/{{id}}/"


class TemplateVariableWrapper(LabsCommonObjectWrapper[TemplateVariableClient, VariableTemplate, VariableTemplateInput]):
    API_CLASS = TemplateVariableClient
    DATA_MODEL = VariableTemplate
    INPUT_CLASS_MODEL = VariableTemplateInput


class TemplateVariablesManagerClient(ManagerApiClient):
    URL = f"{settings.base_url_labs}api/labs/templatevariables/"

    def request_check_unique(self, params: dict):
        return self.api_session.get(url=f"{settings.base_url_labs}api/variable-check-unique/", params=params)


class TemplateVariablesManager(
    LabsCommonManager[TemplateVariablesManagerClient, TemplateVariableWrapper, VariableTemplateInput]
):
    API_CLASS = TemplateVariablesManagerClient
    CREATE_MODEL = VariableTemplateInput
    SINGLE_OBJECT_CLASS = TemplateVariableWrapper

    def create_variable(self, input_data_model: VariableTemplateInput | None = None) -> TemplateVariableWrapper:
        return self.create(input_data_model or VariableTemplateInput())

    def check_unique(self, lab_id, variable_name) -> bool:
        response = self.api.request_check_unique({"lab": lab_id, "variable_name": variable_name})
        response.raise_for_status()
        return response.json()["is_unique"]
