from http import HTTPStatus
from typing import List

import allure
from pydantic import parse_raw_as
from requests import Response
from waiting import wait

from core.api.lms.base import LMSApiObject, LMSApiObjectManager
from core.api.lms.base_api import LmsAsyncApi
from core.models.lms.activity_workflow_aggregate import ActivityByObjectiveWorkflowAndAxis, ActivityWithAggregate
from core.models.lms.lms_base import LMSHasKey, LMSMayHasKey
from core.models.lms.objective_workflow_aggregate import ObjectiveRecord
from core.models.lms.objective_workflow_aggregate import ObjectiveWorkflowAggregate as ObjectiveWorkflowAggregateModel
from core.models.query import LoadOptions
from settings import settings
from util.assertions.common_assertions import assert_response_status


# Looks like this API is not fully functional
class ObjectiveWorkflowAggregateApi(LmsAsyncApi[ObjectiveWorkflowAggregateModel, LMSHasKey, LMSMayHasKey]):
    NAME = "ObjectiveWorkflowAggregate"
    PATH_NAME = "objective-workflow-aggregates"
    URL = f"{settings.base_url_lms_api}{PATH_NAME}"
    MODEL = ObjectiveWorkflowAggregateModel


class ObjectiveWorkflowAggregate(LMSApiObject[ObjectiveWorkflowAggregateModel, ObjectiveWorkflowAggregateApi]):
    API = ObjectiveWorkflowAggregateApi

    def wait_for_progress_update(self):
        initial_progress = getattr(self.data.last_objective_workflow, "progress", 0.0)

        def condition_function():
            self.sync()
            return self.data.last_objective_workflow.progress > initial_progress

        return wait(
            condition_function,
            timeout_seconds=settings.default_command_timeout,
            sleep_seconds=settings.default_command_sleep,
            waiting_for="Objective workflow progress to be updated",
        )

    def request_get_activity_with_aggregates(self) -> Response:
        return self.session.get(f"{self._api.get_instance_url(self.data.id)}/activity-with-aggregates")

    def get_activity_with_aggregates(self) -> ActivityWithAggregate:
        with allure.step(f"Get activity with aggregate for {self.data.id} objective workflow aggregate"):
            response = self.request_get_activity_with_aggregates()
            assert_response_status(response.status_code, HTTPStatus.OK)

            return parse_raw_as(ActivityWithAggregate, response.text)

    def request_get_activity_by_owa_axis(self, axis: str) -> Response:
        return self._api.session.get(f"{self._api.get_instance_url(self.data.id)}/activity/{axis}")

    def get_activity_by_owa_axis(self, axis: str) -> ActivityByObjectiveWorkflowAndAxis:
        with allure.step(f"Get activity axis={axis} for objective workflow aggregate id={self.data.id}"):
            response = self.request_get_activity_by_owa_axis(axis)
            assert_response_status(response.status_code, HTTPStatus.OK)

            return parse_raw_as(ActivityByObjectiveWorkflowAndAxis, response.text)

    def get_objective_records(self) -> List[ObjectiveRecord]:
        with allure.step(f"Get objective records for objective workflow aggregate ID: {self.data.id}"):
            response = self.request_get_objective_records()
            assert_response_status(response.status_code, HTTPStatus.OK)

            return parse_raw_as(List[ObjectiveRecord], response.text)

    def request_get_objective_records(self) -> List[ObjectiveRecord]:
        return self.session.get(f"{self._api.get_instance_url(self.data.id)}/objective-records")


class ObjectiveWorkflowAggregateFactory(LMSApiObjectManager[ObjectiveWorkflowAggregateApi, ObjectiveWorkflowAggregate]):
    API = ObjectiveWorkflowAggregateApi
    OBJECT = ObjectiveWorkflowAggregate

    def wait_for_objective(self, objective_id: str):
        return wait(
            lambda: self.query(load_options=LoadOptions(filter=f'["objective.id","=","{objective_id}"]')),
            timeout_seconds=settings.default_command_timeout,
            sleep_seconds=settings.default_command_sleep,
            waiting_for=f"Objective workflow aggregate to appear for objective with id {objective_id}",
        )
