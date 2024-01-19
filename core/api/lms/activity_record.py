import allure

from core.api.lms.base import LMSApiObject, LMSApiObjectManager
from core.api.lms.base_api import LmsAsyncApi
from core.models.lms.activity_workflow_aggregate import ActivityRecord as ActivityRecordsModel
from core.models.query import LoadOptions
from settings import settings
from util.helpers import first

# TODO: Create & Update ActivityRecord will be handled later


class ActivityRecordsApi(LmsAsyncApi[ActivityRecordsModel, None, None]):
    NAME = "ActivityRecords"
    PATH_NAME = "activity-records"
    URL = f"{settings.base_url_lms_api}{PATH_NAME}"
    MODEL = ActivityRecordsModel


class ActivityRecord(LMSApiObject[ActivityRecordsModel, ActivityRecordsApi]):
    API = ActivityRecordsApi


class ActivityRecordsFactory(LMSApiObjectManager[ActivityRecordsApi, ActivityRecord]):
    API = ActivityRecordsApi
    OBJECT = ActivityRecord

    def get_activity_record_by_activity_workflow_id(self, id: str) -> ActivityRecord | None:
        with allure.step(f"Get activity record by ID: {id}"):
            load_options = LoadOptions(take=1, filter=f'["activityWorkflowId","=","{id}"]')
            query_result = self.query(load_options)
            return first(query_result).data
