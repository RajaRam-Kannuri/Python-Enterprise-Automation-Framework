import allure
from waiting import wait

from core.api.lms.base import LMSApiObject, LMSApiObjectManager
from core.api.lms.base_api import LmsAsyncApi
from core.models.lms.activity_workflow_aggregate import ActivityWorkflow as ActivityWorkflowModel
from core.models.lms.activity_workflow_aggregate import FinishActivityWorkflow, StartActivityWorkflow
from core.models.lms.lms_base import LMSHasKey, LMSMayHasKey
from core.models.lms.objective_workflow_aggregate import ObjectiveWorkflow, WorkflowState
from settings import settings


class ActivityWorkflowApi(LmsAsyncApi[ActivityWorkflowModel, LMSMayHasKey, LMSHasKey]):
    NAME = "ActivityWorkflow"
    PATH_NAME = "activity-workflows"
    URL = f"{settings.base_url_lms_api}{PATH_NAME}"
    MODEL = ActivityWorkflowModel

    def start(self, payload: StartActivityWorkflow):
        url = f"{settings.base_url_lms_api}start-activity-workflows"

        command = self._send_async_request(url, payload)
        return self.get(command.entity_id)

    def finish(self, payload: FinishActivityWorkflow):
        url = f"{settings.base_url_lms_api}finish-activity-workflows"

        command = self._send_async_request(url, payload)
        return self.get(command.entity_id)


class ActivityWorkflow(LMSApiObject[ActivityWorkflowModel, ActivityWorkflowApi]):
    API = ActivityWorkflowApi

    def wait_for_activity_workflow_to_finish(self):
        with allure.step(f"Waiting for activity workflow ID={self.data.id} to finish"):
            return wait(
                lambda: self.data.state == WorkflowState.FINISHED,
                on_poll=self.sync,
                timeout_seconds=settings.default_command_timeout,
                sleep_seconds=settings.default_command_sleep,
                waiting_for=f"Activity workflow ID={self.data.id} to finish",
            )

    def finish(self, objective_workflow: ObjectiveWorkflow):
        with allure.step(f"Finish Activity Workflow with ID={self.data.id}"):
            payload = FinishActivityWorkflow(
                objective_workflow_id=objective_workflow.id, activity_workflow_ids=[self.data.id]
            )
            self._api.finish(payload)


class ActivityWorkflowManager(LMSApiObjectManager[ActivityWorkflowApi, ActivityWorkflow]):
    API = ActivityWorkflowApi
    OBJECT = ActivityWorkflow

    def start(self, objective_workflow: ObjectiveWorkflow, activity_part_ids: list[str] | None = None):
        with allure.step(f"Start Activity Workflow for objective workflow ID={objective_workflow.id}"):
            payload = StartActivityWorkflow(
                objective_workflow_id=objective_workflow.id, activity_part_ids=activity_part_ids
            )
            api_result = self._api.start(payload)

        return self.OBJECT(self.session, api_result)
