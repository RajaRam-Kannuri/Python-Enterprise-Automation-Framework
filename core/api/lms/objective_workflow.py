from http import HTTPStatus

import allure
from requests import Response
from waiting import wait

from core.api.base_api import prepare_body
from core.api.lms.base import LMSApiObject, LMSApiObjectManager
from core.api.lms.base_api import LmsAsyncApi
from core.models.lms.lms_base import LMSHasKey, LMSMayHasKey
from core.models.lms.objective_workflow_aggregate import FinishObjectiveWorkflow
from core.models.lms.objective_workflow_aggregate import ObjectiveWorkflow as ObjectiveWorkflowModel
from core.models.lms.objective_workflow_aggregate import (
    ObjectiveWorkflowAggregate,
    StartObjectiveWorkflow,
    WorkflowState,
)
from core.models.lti.lti_resource_library import LtiResourceInitModel, LtiResourceLinkModel
from settings import settings
from util.assertions.common_assertions import assert_response_status


class ObjectiveWorkflowApi(LmsAsyncApi[ObjectiveWorkflowModel, LMSMayHasKey, LMSHasKey]):
    NAME = "ObjectiveWorkflow"
    PATH_NAME = "objective-workflows"
    URL = f"{settings.base_url_lms_api}{PATH_NAME}"
    MODEL = ObjectiveWorkflowModel

    def start(self, payload: StartObjectiveWorkflow):
        url = f"{settings.base_url_lms_api}start-objective-workflows"

        command = self._send_async_request(url, payload)
        return self.get(command.entity_id)

    def finish(self, payload: FinishObjectiveWorkflow):
        url = f"{settings.base_url_lms_api}finish-objective-workflows"

        command = self._send_async_request(url, payload)
        return self.get(command.entity_id)

    def request_get_lti_form(self, payload: LtiResourceLinkModel, obj_id) -> Response:
        url = f"{self.get_instance_url(obj_id)}/resource-link"
        return self.session.post(url=url, data=prepare_body(payload), headers={"Content-type": "application/json"})

    def get_lti_form_from_workflow(self, obj_id, payload) -> LtiResourceInitModel:
        with allure.step(f"Get LTI Form for Objective Workflow with ID={obj_id}"):
            response = self.request_get_lti_form(payload, obj_id)
            assert_response_status(response.status_code, HTTPStatus.OK)

            return LtiResourceInitModel.parse_raw(response.text)


class ObjectiveWorkflow(LMSApiObject[ObjectiveWorkflowModel, ObjectiveWorkflowApi]):
    API = ObjectiveWorkflowApi

    def wait_for_objective_workflow_to_finish(self):
        with allure.step(f"Waiting for objective workflow ID={self.data.id} to finish"):
            return wait(
                lambda: self.data.state == WorkflowState.FINISHED,
                on_poll=self.sync,
                # TODO: remove multiplication after fix of
                #  https://youtrack.constr.dev/issue/ALMS-5740/Finish-composite-workflow-synchronously-for-LTI-children
                timeout_seconds=settings.default_command_timeout * 2,
                sleep_seconds=settings.default_command_sleep,
                waiting_for=f"Objective workflow ID={self.data.id} to finish",
            )

    def finish(self):
        with allure.step(f"Finish Objective Workflow with ID={self.data.id}"):
            payload = FinishObjectiveWorkflow(objective_workflow_id=self.data.id)
            self._api.finish(payload)

    def get_lti_form(self, payload: LtiResourceLinkModel):
        return self._api.get_lti_form_from_workflow(self.id, payload)


class ObjectiveWorkflowManager(LMSApiObjectManager[ObjectiveWorkflowApi, ObjectiveWorkflow]):
    API = ObjectiveWorkflowApi
    OBJECT = ObjectiveWorkflow

    def start(self, objective_workflow_aggregate: ObjectiveWorkflowAggregate):
        with allure.step(f"Start Objective Workflow with ID={objective_workflow_aggregate.id}"):
            payload = StartObjectiveWorkflow(objective_workflow_aggregate_id=objective_workflow_aggregate.id)
            api_result = self._api.start(payload)

            return self.OBJECT(self.session, api_result)
