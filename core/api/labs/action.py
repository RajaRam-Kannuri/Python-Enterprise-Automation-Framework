from core.api.base_refactored.api_client import ManagerApiClient, SingleItemApiClient
from core.api.labs.base import LabsCommonManager, LabsCommonObjectWrapper
from core.models.labs.actions import SessionAction, SessionActionInput
from settings import settings


class ActionClient(SingleItemApiClient):
    NAME = "life-cycle action"
    URL_TEMPLATE = f"{settings.base_url_labs}api/labs/actions/{{id}}/"


class ActionWrapper(LabsCommonObjectWrapper[ActionClient, SessionAction, SessionActionInput]):
    API_CLASS = ActionClient
    DATA_MODEL = SessionAction
    INPUT_CLASS_MODEL = SessionActionInput


class ActionsManagerClient(ManagerApiClient):
    URL = f"{settings.base_url_labs}api/labs/actions/"


class ActionsManager(LabsCommonManager[ActionsManagerClient, ActionWrapper, SessionActionInput]):
    API_CLASS = ActionsManagerClient
    SINGLE_OBJECT_CLASS = ActionWrapper
    CREATE_MODEL = SessionActionInput

    def create_session_action(self, input_data_model: SessionActionInput = None) -> ActionWrapper:
        return self.create(input_data_model or SessionActionInput())

    def create_session_action_with_name(self, name: str) -> ActionWrapper:
        return self.create(SessionActionInput(name=name))
