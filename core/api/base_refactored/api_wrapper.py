import abc
import enum
import http
import logging
from abc import ABC
from typing import Generic, List, Type, TypeVar

import allure
import requests
from pydantic import BaseModel
from requests import Response, Session
from waiting import wait

from core.api.base_refactored.api_client import ManagerApiClient, SingleItemApiClient
from settings import settings
from util.api.allure_reporting import prettify_dict
from util.assertions import common_assertions

ApiWrap = TypeVar("ApiWrap", bound="ApiWrapper")
DataModel = TypeVar("DataModel", bound=BaseModel)
PatchModel = TypeVar("PatchModel", bound=BaseModel)
PutModel = TypeVar("PutModel", bound=BaseModel)
CreateModel = TypeVar("CreateModel", bound=BaseModel)
SingleClient = TypeVar("SingleClient", bound="SingleItemApiClient")
ManagerClient = TypeVar("ManagerClient", bound="ManagerApiClient")


class ApiWrapper(Generic[SingleClient, DataModel], ABC):
    """
    This is a base class for API wrappers. This object provides a convenient way to work with a concrete API object.
    It has an object data (self.data) as a corresponding model instance and updates it after each request.
    """

    DATA_MODEL: Type[DataModel]
    DEFAULT_TEARDOWN_TIMEOUT = settings.default_api_timeout
    API_CLASS: Type[SingleClient]
    NAME_KEY_IN_PAYLOAD = "name"

    def __init__(
        self,
        api_session: Session,
        data: dict | DataModel | None = None,
        object_id: int | str | None = None,
        api: SingleClient | None = None,
    ):
        if not (data or object_id):
            raise RuntimeError("Either data or object_id should be provided")
        if data and object_id:
            raise RuntimeError("Either data or object_id should be provided, not both")

        self.data: DataModel = self.DATA_MODEL(**data) if isinstance(data, dict) else data
        self.teardown_timeout = self.DEFAULT_TEARDOWN_TIMEOUT
        self.id = object_id or self.data.id
        self.api: SingleClient = api
        if api is None:
            self.api: SingleClient = self.API_CLASS(api_session=api_session, object_id=self.id)
        self.previous_data: DataModel | None = None
        self.is_exist_on_backend: bool = True
        self.originally_was_created_with: DataModel | None = None
        self.latest_response: requests.Response | None = None

    @property
    def api_session(self):
        return self.api.api_session

    def __str__(self):
        return f"a wrapper for {self.api}"

    def __eq__(self, other) -> bool:
        return self.data == other.data

    @property
    @abc.abstractmethod
    def is_finalized(self) -> bool:
        ...

    def _update_inner_data(self, response: requests.Response):
        data = response.json()
        self.latest_response = response
        if data in ({}, None) and self.data is None:
            return
        self.previous_data = self.data
        self.data = self.DATA_MODEL(**data)

    @property
    def name(self):
        return getattr(self.data, self.NAME_KEY_IN_PAYLOAD, None) or getattr(
            self.previous_data, self.NAME_KEY_IN_PAYLOAD
        )


class DeletableWrapper(ApiWrapper[SingleClient, DataModel], Generic[SingleClient, DataModel]):
    """
    A wrapper for an object that can be deleted to provide handy teardown methods.
    """

    @property
    def is_finalized(self):
        return not self.is_exist_on_backend

    def delete(self):
        response = self.api.request_delete()
        response.raise_for_status()
        self.is_exist_on_backend = False
        return response

    def make_deleted(self):
        """requests delete if an object isn't deleted yet"""
        if self.is_exist_on_backend:
            logging.debug(f"deleting {self}...")
            self.delete()

    def teardown(self):
        """A general teardown method"""
        logging.debug(f"finalizing {self}...")
        self.make_deleted()


class PatchableWrapper(ApiWrapper[SingleClient, DataModel], Generic[SingleClient, DataModel, PatchModel]):
    INPUT_CLASS_MODEL: type[PatchModel]

    @classmethod
    def generate_random_data(cls) -> DataModel:
        return cls.INPUT_CLASS_MODEL.construct()

    def patch(self, update_data: PatchModel) -> requests.Response:
        response = self.api.request_patch(update_data)
        response.raise_for_status()
        self._update_inner_data(response)
        return response


class PuttableWrapper(ApiWrapper[SingleClient, DataModel], Generic[SingleClient, DataModel, PutModel]):
    INPUT_CLASS_MODEL: type[PutModel]

    @classmethod
    def generate_random_data(cls) -> DataModel:
        return cls.INPUT_CLASS_MODEL.construct()

    def put(self, update_data: PutModel) -> requests.Response:
        response = self.api.request_put(update_data)
        response.raise_for_status()
        self._update_inner_data(response)
        return response


class GettableWrapper(ApiWrapper[SingleClient, DataModel], Generic[SingleClient, DataModel]):
    def fetch_data(self) -> requests.Response:
        response = self.api.request_get()

        # a special case for 404 without an exception
        if response.status_code == http.HTTPStatus.NOT_FOUND:
            self.is_exist_on_backend = False
            self.latest_response = response

            # if the data for a deleted object is fetched again, we still want to have a previous_data
            if self.data is not None:
                self.previous_data = self.data
                self.data = None
            return response

        response.raise_for_status()
        self._update_inner_data(response)
        return response


class SelfStateChangingWrapper(ApiWrapper[SingleClient, DataModel], Generic[SingleClient, DataModel]):
    """
    A wrapper for an object that can change its state/status (or some other field depending on what developers
     decided to name it).
     This wrapper provides a general wait_for_state method that waits until the object is in a desired state/status.
    Some objects, for example, can be finalized by deleting them (DeletableWrapper). This type is finalized by changing
    its state/status to a terminal one.
    The idea is to have a general teardown method, that finalizes the object.
    """

    TERMINAL_STATES: set
    STATE_KEY = "status"

    @property
    @abc.abstractmethod
    def states(self) -> enum.StrEnum:
        ...

    @property
    def state(self):
        return getattr(self.data, self.STATE_KEY, None)

    @property
    def is_in_terminal_state(self) -> bool:
        return self.state in self.TERMINAL_STATES

    @property
    def is_finalized(self):
        return not self.is_exist_on_backend or self.is_in_terminal_state

    def wait_for_state(self, desired_state: states, timeout=settings.default_api_timeout) -> Response:
        """
        Wait until SelfStateChangingObject is in state/status {desired_state}
        """
        state_value = desired_state.value

        def request_get_for_a_status():
            get_response = self.api.request_get()
            result = get_response if get_response.json()[self.STATE_KEY] == state_value else False
            return result

        with allure.step(f'Waiting until {self.api.NAME} is in {self.STATE_KEY} "{state_value}"'):
            response = wait(
                request_get_for_a_status,
                waiting_for=f'until {self.api.NAME} is in {self.STATE_KEY} "{state_value}"',
                timeout_seconds=timeout,
            )
        self._update_inner_data(response)
        return response


class WrappersManager(Generic[ManagerClient, ApiWrap], ABC):
    """
    This is a base class for API managers. These types of objects are the source of API wrappers.
    """

    API_CLASS: type[ManagerClient]
    SINGLE_OBJECT_CLASS: type[ApiWrap]

    def __init__(self, api_session: Session):
        self.api: ManagerClient = self.API_CLASS(api_session=api_session)

    @property
    def api_session(self) -> Session:
        return self.api.api_session


class CreatablesManager(WrappersManager[ManagerClient, ApiWrap], Generic[ManagerClient, ApiWrap, CreateModel]):
    CREATE_MODEL = type[CreateModel]

    def create(self, data: DataModel = None) -> ApiWrap:
        """Creates an object of self.SINGLE_OBJECT_CLASS with random data, updated by non_default_data

        Args:
            data: data to create an object of self.SINGLE_OBJECT_CLASS type with.

        Returns: created object of self.SINGLE_OBJECT_CLASS type

        """
        if data is None:
            data = self.CREATE_MODEL()
        non_default_data = data.dict(exclude_unset=True)
        object_element_name = (
            getattr(data, self.SINGLE_OBJECT_CLASS.NAME_KEY_IN_PAYLOAD, None)
            or str(non_default_data)
            or "random_generated"
        )
        logging.info(f"creating {self.SINGLE_OBJECT_CLASS.API_CLASS.NAME} {object_element_name}")
        with allure.step(
            f"creating {self.SINGLE_OBJECT_CLASS.API_CLASS.NAME}"
            f" with not default data={prettify_dict(non_default_data)}"
        ):
            response = self.api.request_post(data.dict())
        common_assertions.assert_response_status(response.status_code, http.HTTPStatus.CREATED)
        single_object = self.SINGLE_OBJECT_CLASS(self.api_session, response.json())
        single_object.originally_was_created_with = data
        return single_object


class QueryablesManager(WrappersManager[ManagerClient, ApiWrap], Generic[ManagerClient, ApiWrap]):
    def get_list(self, search_query: dict | None = None, max_objects=100) -> List[ApiWrap]:
        response = self.api.request_query(params=search_query or {})
        response.raise_for_status()
        assert (
            len(response.json()) <= max_objects
        ), f'Too many objects "{self.SINGLE_OBJECT_CLASS}" in a response: {(len(response.json()))}'
        result = [self.SINGLE_OBJECT_CLASS(api_session=self.api_session, data=item) for item in response.json()]
        return result

    def get_list_with_pagination(
        self, search_query: dict | None = None, limit: int = 10, max_objects=100
    ) -> List[ApiWrap]:
        """

        Args:
            search_query: search query, see swagger documentation
            limit: how many objects to query
            max_objects: a safe measure to prevent accidental querying and parsing too many objects

        Returns:
            a list of requested objects

        """
        params = {"limit": limit}
        params.update(search_query or {})
        response = self.api.request_query(params=params)
        response.raise_for_status()
        objects_list = response.json()["results"]
        assert (
            len(response.json()) <= max_objects
        ), f'Too many objects "{self.SINGLE_OBJECT_CLASS}" in a response: {(len(objects_list))}'
        result = [self.SINGLE_OBJECT_CLASS(api_session=self.api_session, data=item) for item in objects_list]
        return result
