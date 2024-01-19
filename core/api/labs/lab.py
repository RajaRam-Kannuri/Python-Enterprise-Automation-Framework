import logging
from functools import cached_property
from typing import Self

import allure
import requests
from assertpy import assert_that
from faker import Faker
from requests import HTTPError

from core.api.base_refactored.api_client import ManagerApiClient, SingleItemApiClient
from core.api.labs.base import LabsCommonManager, LabsCommonObjectWrapper
from core.api.labs.workspace_configuration import WorkspaceConfigWrapper
from core.models.labs.lab import LabDetailed, LabInput
from settings import settings
from util.random import random_string

fake = Faker("en_US")


class LabClient(SingleItemApiClient):
    NAME = "lab"
    URL_TEMPLATE = f"{settings.base_url_labs}api/labs/{{id}}/"

    def request_publish(self) -> requests.Response:
        with allure.step(f"publishing {self}"):
            response = self.api_session.post(url=f"{self.url}publish/")
            return response

    def request_unpublish(self) -> requests.Response:
        with allure.step(f"unpublishing {self}"):
            response = self.api_session.post(url=f"{self.url}unpublish/")
            return response

    def request_copy(self, payload: dict) -> requests.Response:
        with allure.step(f'copying {self} with a new data="{payload}"'):
            response = self.api_session.post(url=f"{self.url}clone/", json=payload)
            return response

    def request_approve_translations(self, data: dict) -> requests.Response:
        with allure.step(f"Approve translations in {self}"):
            response = self.api_session.post(url=f"{self.url}approve_translations/", json=data)
            return response

    def request_post_language(self, payload: dict) -> requests.Response:
        with allure.step(f"adding language to {self}"):
            response = self.api_session.post(url=f"{self.url}add_language/", json=payload)
            return response


class LabWrapper(LabsCommonObjectWrapper[LabClient, LabDetailed, LabInput]):
    DATA_MODEL = LabDetailed
    INPUT_CLASS_MODEL = LabInput
    API_CLASS = LabClient

    @property
    def is_published(self):
        return getattr(self.data, "is_public")

    @property
    def workspace_configuration(self):
        return WorkspaceConfigWrapper(api_session=self.api_session, object_id=self.data.workspace_configuration)

    @cached_property
    def tasks_manager(self):
        from core.api.labs.task import TasksInLabManager

        return TasksInLabManager(self)

    def to_subsequent_from(self, lab: Self) -> requests.Response:
        response = self.patch({"previous_id": lab.id})
        response.raise_for_status()
        self._update_inner_data(response)
        return response

    def add_language(self, lang_code: str) -> requests.Response:
        language_payload = {"language_code": lang_code}
        response = self.api.request_post_language(payload=language_payload)
        response.raise_for_status()
        self._update_inner_data(response)
        return response

    def to_independent(self) -> requests.Response:
        response = self.patch({"previous_id": None})
        response.raise_for_status()
        self._update_inner_data(response)
        return response

    def publish(self) -> requests.Response:
        response = self.api.request_publish()
        response.raise_for_status()
        self._update_inner_data(response)
        return response

    def unpublish(self) -> requests.Response:
        response = self.api.request_unpublish()
        response.raise_for_status()
        self._update_inner_data(response)
        return response

    def make_deleted(self):
        if self.is_exist_on_backend:
            self.make_unpublished()
            try:
                self.delete()
            except HTTPError as error:
                if error.response.status_code == 403:
                    logging.debug("Lab deletion error. Retrying deletion with forced unpublishing")
                    self.unpublish()
                    self.delete()
                else:
                    raise error

    def make_unpublished(self):
        if self.is_published:
            self.unpublish()

    def make_published(self):
        if not self.is_published:
            self.publish()

    def copy(self, new_lab_name: str = None) -> Self:
        if new_lab_name is None:
            new_lab_name = f"{self.name} copy"
        response = self.api.request_copy(payload={"name": new_lab_name})
        response.raise_for_status()
        return LabWrapper(api_session=self.api_session, data=response.json())

    def add_contact(self, name: str | None = None, email: str | None = None, phone: str | None = None) -> dict:
        contact_payload = {
            "name": name if name is not None else fake.name(),
            "email": email if email is not None else fake.email(),
            "phone": phone if phone is not None else fake.phone_number(),
        }
        self.patch({"contacts": [*self.data.contacts, contact_payload]})
        return contact_payload

    def add_link(self, name: str | None = None, url: str | None = None) -> dict:
        link_payload = {
            "name": name if name is not None else random_string(20),
            "url": url if url is not None else fake.url(),
        }
        self.patch({"links": [*self.data.links, link_payload]})
        return link_payload

    def add_description_with_text(self, description_text: str) -> dict:
        description_payload = {
            "type": "doc",
            "content": [{"type": "paragraph", "content": [{"type": "text", "text": description_text}]}],
        }
        self.patch({"data": description_payload})
        return description_payload

    def attach_variable(self, variable_id: str, variable_name: str) -> requests.Response:
        old_variables = [
            pregeneratevariable.to_input_type().dict() for pregeneratevariable in self.data.pregeneratevariables
        ]
        response = self.patch(
            {"pregenvariables": [*old_variables, {"template": variable_id, "varname": variable_name}]}
        )
        return response

    def remove_variable(self, variable_id: str) -> requests.Response:
        variables_dict = {
            variable.template.id: variable.to_input_type().dict() for variable in self.data.pregeneratevariables
        }
        assert variable_id in variables_dict, f'variable id "{variable_id}" is not in the current lab!'

        variables_dict.pop(variable_id)
        response = self.patch({"pregenvariables": list(variables_dict.values())})

        return response


class LabsManagerClient(ManagerApiClient):
    URL = f"{settings.base_url_labs}api/labs/"


class LabsManager(LabsCommonManager[LabsManagerClient, LabWrapper, LabInput]):
    CREATE_MODEL = LabInput
    SINGLE_OBJECT_CLASS = LabWrapper
    API_CLASS = LabsManagerClient

    def create_lab(self, input_data_model: LabInput) -> LabWrapper:
        return self.create(input_data_model)

    def get_lab(self, search_query: dict) -> LabWrapper:
        result = self.get_list(search_query, max_objects=1)[0]
        return result

    def get_lab_by_name(self, name, exact_text=True) -> LabWrapper:
        results: list = self.get_list(search_query={"name": name})
        if exact_text:
            results = list(filter(lambda lab: lab.name == name, results))
        assert_that(len(results)).is_equal_to(1)
        return results.pop()
