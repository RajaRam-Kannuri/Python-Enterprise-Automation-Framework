from typing import Generic, TypeVar

from core.api.base import ApiObject, ApiObjectManager, DeletableApiObject, UpdatableApiObject
from core.api.base_api import ApiModel
from core.api.lms.base_api import LmsAsyncApi
from core.models.query import LoadOptions

LMSApiType = TypeVar("LMSApiType", bound=LmsAsyncApi)


class LMSApiObject(
    Generic[ApiModel, LMSApiType],
    UpdatableApiObject[ApiModel, LMSApiType],
    DeletableApiObject[ApiModel, LMSApiType],
    ApiObject[ApiModel, LMSApiType],
):
    API: LMSApiType


LMSObjectType = TypeVar("LMSObjectType", bound=LMSApiObject)


class LMSApiObjectManager(ApiObjectManager[LMSApiType, LMSObjectType]):
    API: type[LMSApiType]
    OBJECT: type[LMSObjectType]

    def query(self, load_options: LoadOptions) -> list[LMSObjectType]:
        query_response = self._api.query(load_options)
        return [self.OBJECT(self.session, data) for data in query_response.data]
