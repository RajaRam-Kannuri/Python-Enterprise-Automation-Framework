from core.api.base_refactored.api_client import ManagerApiClient, SingleItemApiClient
from core.api.labs.base import LabsCommonManager, LabsCommonObjectWrapper
from core.models.labs.scriptproject import ScriptProject, ScriptProjectInput
from settings import settings


class ScriptProjectClient(SingleItemApiClient):
    NAME = "script project"
    URL_TEMPLATE = f"{settings.base_url_labs}api/labs/scriptprojects/{{id}}/"


class ScriptProjectWrapper(LabsCommonObjectWrapper[ScriptProjectClient, ScriptProject, ScriptProjectInput]):
    API_CLASS = ScriptProjectClient
    DATA_MODEL = ScriptProject
    INPUT_CLASS_MODEL = ScriptProjectInput


class ScriptProjectsManagerClient(ManagerApiClient):
    URL = f"{settings.base_url_labs}api/labs/scriptprojects/"


class ScriptProjectsManager(LabsCommonManager[ScriptProjectsManagerClient, ScriptProjectWrapper, ScriptProjectInput]):
    API_CLASS = ScriptProjectsManagerClient
    SINGLE_OBJECT_CLASS = ScriptProjectWrapper
    CREATE_MODEL = ScriptProjectInput

    def create_script_project(self, input_data_model: ScriptProjectInput) -> ScriptProjectWrapper:
        return self.create(input_data_model)
