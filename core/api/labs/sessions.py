from typing import Type

import requests

from core.api.base_refactored.api_client import ManagerApiClient, SingleItemApiClient
from core.api.base_refactored.api_wrapper import (
    GettableWrapper,
    PatchableWrapper,
    PuttableWrapper,
    SelfStateChangingWrapper,
)
from core.api.labs.base import LabsCommonManager
from core.models.labs.session import Session, SessionInput, SessionStates
from settings import settings


class SessionClient(SingleItemApiClient):
    NAME = "session"
    URL_TEMPLATE = f"{settings.base_url_labs}api/sessions/{{id}}/"

    def request_start(self) -> requests.Response:
        return self.api_session.post(f"{self.url}start/")

    def request_pause(self) -> requests.Response:
        return self.api_session.post(f"{self.url}pause/")

    def request_resume(self) -> requests.Response:
        return self.api_session.post(f"{self.url}resume/")

    def request_finish(self) -> requests.Response:
        return self.api_session.post(f"{self.url}finish/")

    def request_reset(self, data: dict) -> requests.Response:
        return self.api_session.post(f"{self.url}reset/", json=data)


class SessionWrapper(
    PatchableWrapper[SessionClient, Session, SessionInput],
    PuttableWrapper[SessionClient, Session, SessionInput],
    GettableWrapper[SessionClient, Session],
    SelfStateChangingWrapper[SessionClient, Session],
):
    API_CLASS = SessionClient
    DATA_MODEL = Session
    INPUT_CLASS_MODEL = SessionInput
    STATE_KEY = "state"

    @property
    def states(self) -> Type[SessionStates]:
        return SessionStates

    def start(self, wait_for_desired_status=True) -> requests.Response:
        response = self.api.request_start()
        if wait_for_desired_status:
            response = self.wait_for_state(self.states.ACTIVE)
        response.raise_for_status()
        return response

    def pause(self) -> requests.Response:
        response = self.api.request_pause()
        response.raise_for_status()
        self._update_inner_data(response)
        return response

    def resume(self) -> requests.Response:
        response = self.api.request_resume()
        response.raise_for_status()
        self._update_inner_data(response)
        return response

    def finish(self, wait_for_desired_status=True):
        response = self.api.request_finish()
        if wait_for_desired_status:
            response = self.wait_for_state(self.states.FINISHED)
        response.raise_for_status()
        return response

    def reset(self, reset_vm=True, reset_lab=True) -> requests.Response:
        """By default, resets session and a lab (as it is on web)"""
        response = self.api.request_reset({"reset_vm": reset_vm, "reset_lab": reset_lab})
        response.raise_for_status()
        self._update_inner_data(response)
        return response

    def make_finished(self):
        if self.state != self.states.FINISHED:
            self.finish()

    def teardown(self):
        self.make_finished()


class SessionManagerClient(ManagerApiClient):
    URL = f"{settings.base_url_labs}api/sessions/"


class SessionManager(LabsCommonManager[SessionManagerClient, SessionWrapper, SessionInput]):
    API_CLASS = SessionManagerClient
    SINGLE_OBJECT_CLASS = SessionWrapper
    CREATE_MODEL = SessionInput

    def create_session(self, input_data_model: SessionInput) -> SessionWrapper:
        return self.create(input_data_model)
