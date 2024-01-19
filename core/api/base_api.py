import json
from http import HTTPStatus
from typing import ClassVar, Generic, Protocol, TypeVar, runtime_checkable

import allure
from pydantic import BaseModel, parse_raw_as
from requests import Response, Session

from core.models.lms.lms_base import LMSModelBase
from core.models.query import LoadOptions, QueryResponse
from util.assertions.common_assertions import assert_response_status


@runtime_checkable
class EntityProtocol(Protocol):
    id: str


DataPayload = TypeVar("DataPayload", BaseModel, dict, str)
ApiModel = TypeVar("ApiModel", bound=EntityProtocol)
CreateApiModel = TypeVar("CreateApiModel", bound=BaseModel)
UpdateApiModel = TypeVar("UpdateApiModel", bound=BaseModel)


def prepare_body(payload: DataPayload, exclude_unset=False) -> str:
    if isinstance(payload, LMSModelBase):
        data = payload.lms_json(exclude_unset=exclude_unset)
    elif isinstance(payload, BaseModel):
        data = payload.json(exclude_unset=exclude_unset)
    elif isinstance(payload, dict):
        data = json.dumps(payload)
    else:
        data = str(payload)

    return data


class ObjectApi(Generic[ApiModel]):
    MODEL: type[ApiModel]

    URL: ClassVar[str]
    NAME: ClassVar[str]
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def get_instance_url(self, obj_id: str) -> str:
        return f"{self.URL}/{obj_id}"


class ObjectGettableApi(ObjectApi[ApiModel]):
    def request_get(self, obj_id: str) -> Response:
        return self.session.get(self.get_instance_url(obj_id))

    def get(self, obj_id: str) -> ApiModel:
        with allure.step(f"Get {self.NAME} with id: {obj_id}"):
            response = self.request_get(obj_id)
            check_response(response, HTTPStatus.OK)

            return self.MODEL.parse_raw(response.text)

    def request_list(self) -> Response:
        return self.session.get(self.URL)

    def list(self) -> list[ApiModel]:
        with allure.step(f"Get all {self.NAME}"):
            response = self.request_list()
            assert_response_status(response.status_code, HTTPStatus.OK)

            return parse_raw_as(list[self.MODEL], response.text)


class ObjectCreatableApi(ObjectApi[ApiModel], Generic[CreateApiModel, ApiModel]):
    def request_post(self, payload: DataPayload) -> Response:
        return self.session.post(url=self.URL, data=prepare_body(payload), headers={"Content-type": "application/json"})

    def post(self, create_data: CreateApiModel) -> ApiModel:
        with allure.step(f"Creating {self.NAME}"):
            response = self.request_post(create_data)
            assert_response_status(response.status_code, HTTPStatus.OK)

            return self.MODEL.parse_raw(response.text)


class ObjectUpdateableApi(ObjectApi[ApiModel], Generic[UpdateApiModel, ApiModel]):
    def request_put(self, obj_id: str, payload: DataPayload) -> Response:
        return self.session.put(
            url=self.get_instance_url(obj_id),
            data=prepare_body(payload, exclude_unset=True),
            headers={"Content-type": "application/json"},
        )

    def put(self, obj_id: str, data: UpdateApiModel) -> ApiModel:
        with allure.step(f"Update {self.NAME} with id: {obj_id}"):
            response = self.request_put(obj_id, data)
            check_response(response, HTTPStatus.OK)

            return self.MODEL.parse_raw(response.text)


class ObjectDeleteableApi(ObjectApi):
    def request_delete(self, obj_id: str) -> Response:
        return self.session.delete(self.get_instance_url(obj_id))

    def delete(self, obj_id: str):
        with allure.step(f"Delete {self.NAME} with id: {obj_id}"):
            response = self.request_delete(obj_id)
            check_response(response, HTTPStatus.OK)


def check_response(response: Response, expected_code: HTTPStatus | int):
    if response.status_code == HTTPStatus.NOT_FOUND:
        raise ObjectNotFound()

    # TODO: enrich checks
    assert response.status_code == expected_code


class ObjectNotFound(Exception):
    pass


class ObjectQueryableApi(ObjectApi[ApiModel]):
    def request_query(self, payload: LoadOptions | dict) -> Response:
        params = payload.lms_dict() if isinstance(payload, LoadOptions) else payload
        return self.session.get(f"{self.URL}/query", params=params)

    def query(self, load_options: LoadOptions) -> QueryResponse[ApiModel]:
        response = self.request_query(load_options)
        assert_response_status(response.status_code, HTTPStatus.OK)

        return parse_raw_as(QueryResponse[self.MODEL], response.text)
