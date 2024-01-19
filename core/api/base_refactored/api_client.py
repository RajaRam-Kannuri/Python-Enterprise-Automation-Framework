import abc
from abc import ABC
from functools import cached_property
from typing import TypeVar

import allure
import requests
from pydantic import BaseModel
from requests import Session

from util.api.allure_reporting import prettify_dict

DataPayload = TypeVar("DataPayload", BaseModel, dict, str, None)


def prepare_body(payload: DataPayload, exclude_unset=False) -> dict:
    if isinstance(payload, BaseModel):
        data = payload.dict(exclude_unset=exclude_unset)
    else:
        data = payload

    return data


class ApiClient(ABC):
    def __init__(self, api_session: Session):
        self.api_session: Session = api_session

    @property
    @abc.abstractmethod
    def url(self) -> str:
        ...


class SingleItemApiClient(ApiClient):
    """
    This is a base class for API clients that work with a single item.
    """

    URL_TEMPLATE: str
    NAME: str

    def __init__(self, api_session: Session, object_id: int | str):
        super().__init__(api_session)
        self.id = object_id

    @cached_property
    def url(self):
        return self.URL_TEMPLATE.format(id=self.id)

    def __str__(self):
        return f"{self.NAME}: id={self.id}"

    def request_delete(self) -> requests.Response:
        with allure.step(f"deleting {self}"):
            response = self.api_session.delete(url=self.url)
            return response

    def request_get(self) -> requests.Response:
        with allure.step(f"getting {self}"):
            response = self.api_session.get(url=self.url)
            return response

    def request_put(self, update_data: DataPayload) -> requests.Response:
        with allure.step(f"updating {self}"):
            response = self.api_session.put(url=self.url, json=prepare_body(update_data))
            return response

    def request_patch(self, update_data: DataPayload) -> requests.Response:
        with allure.step(f"updating {self}"):
            response = self.api_session.patch(url=self.url, json=prepare_body(update_data))
            return response


class ManagerApiClient(ApiClient):
    """
    This is a base class for API clients that work with static urls to get multiple items.
    """

    URL: str

    def url(self) -> str:
        return self.URL

    def __init__(self, api_session: Session):
        super().__init__(api_session)

    @property
    def name(self) -> str:
        return f"{self.URL.split('/')[-1]}"

    def request_post(self, create_data: DataPayload) -> requests.Response:
        json = prepare_body(create_data)
        with allure.step(f"creating {self.name} with data {prettify_dict(json)}"):
            response = self.api_session.post(self.URL, json=json)
            return response

    def request_query(self, params: dict | None) -> requests.Response:
        with allure.step(f"getting {self.name} with data {prettify_dict(params)}"):
            response = self.api_session.get(self.URL, params=params)
            return response
