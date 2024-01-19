from functools import cached_property
from typing import Any, Generic, TypeVar, Union

from requests import Session

from core.api.base_api import ApiModel, ObjectCreatableApi, ObjectDeleteableApi, ObjectGettableApi, ObjectUpdateableApi
from core.models.lms.lms_base import LMSModelBase

ApiType = TypeVar("ApiType", bound=ObjectGettableApi)


class ApiObject(Generic[ApiModel, ApiType]):
    API: type[ApiType]

    def __init__(self, session: Session, data: ApiModel):
        self.session = session
        self._data = data

    @property
    def data(self) -> ApiModel:
        return self._data

    @cached_property
    def _api(self) -> ApiType:
        return self.API(self.session)

    @property
    def id(self) -> str:
        return self.data.id

    def sync(self):
        self._data = self._api.get(self.id)

    def __eq__(self, other: Any):
        if isinstance(other, ApiObject):
            return self.data == other.data

        if isinstance(other, type(self.data)):
            return self.data == other

        return False


UpdateApiType = TypeVar("UpdateApiType", bound=Union[ObjectGettableApi, ObjectUpdateableApi])


class UpdatableApiObject(ApiObject[ApiModel, UpdateApiType]):
    def put(self, update_data: LMSModelBase):
        self._data = self._api.put(self.id, update_data)


DeleteApiType = TypeVar("DeleteApiType", bound=Union[ObjectGettableApi, ObjectDeleteableApi])


class DeletableApiObject(ApiObject[ApiModel, DeleteApiType]):
    def delete(self):
        return self._api.delete(self.id)


CreateApiType = TypeVar("CreateApiType", bound=ObjectCreatableApi)
ObjectType = TypeVar("ObjectType", bound=ApiObject)


class ApiObjectManager(Generic[CreateApiType, ObjectType]):
    API: type[CreateApiType]
    OBJECT: type[ObjectType]

    def __init__(self, session: Session):
        self.session = session

    @cached_property
    def _api(self) -> CreateApiType:
        return self.API(self.session)

    def get_by_id(self, obj_id: str) -> ObjectType:
        return self.OBJECT(self.session, self._api.get(obj_id))

    def list(self) -> list[ObjectType]:
        return [self.OBJECT(self.session, data) for data in self._api.list()]
