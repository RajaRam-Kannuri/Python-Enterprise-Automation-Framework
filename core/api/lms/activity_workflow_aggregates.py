from waiting import wait

from core.api.lms.base import LMSApiObject, LMSApiObjectManager
from core.api.lms.base_api import LmsAsyncApi
from core.models.lms.activity_workflow_aggregate import ActivityWorkflowAggregate as ActivityWorkflowAggregateModel
from core.models.lms.lms_base import LMSHasKey, LMSMayHasKey
from core.models.query import LoadOptions
from settings import settings


class ActivityWorkflowAggregateApi(LmsAsyncApi[ActivityWorkflowAggregateModel, LMSHasKey, LMSMayHasKey]):
    NAME = "ActivityWorkflowAggregate"
    PATH_NAME = "activity-workflow-aggregates"
    URL = f"{settings.base_url_lms_api}{PATH_NAME}"
    MODEL = ActivityWorkflowAggregateModel


class ActivityWorkflowAggregate(LMSApiObject[ActivityWorkflowAggregateModel, ActivityWorkflowAggregateApi]):
    API = ActivityWorkflowAggregateApi


class ActivityWorkflowAggregateFactory(LMSApiObjectManager[ActivityWorkflowAggregateApi, ActivityWorkflowAggregate]):
    API = ActivityWorkflowAggregateApi
    OBJECT = ActivityWorkflowAggregate

    def wait_for_activity(self, activity_id: str):
        return wait(
            lambda: self.query(load_options=LoadOptions(filter=f'["activity.id","=","{activity_id}"]')),
            timeout_seconds=settings.default_command_timeout,
            sleep_seconds=settings.default_command_sleep,
            waiting_for=f"Activity workflow aggregate to appear for activity with id {activity_id}",
        )

    def get_activity_workflow_aggregate(self, activity_id):
        activity_workflow_aggregates = self.wait_for_activity(activity_id)
        assert len(activity_workflow_aggregates) == 1
        activity_workflow_aggregate = activity_workflow_aggregates[0]
        return activity_workflow_aggregate.data
