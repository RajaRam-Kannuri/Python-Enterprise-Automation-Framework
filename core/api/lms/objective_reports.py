from http import HTTPStatus

import allure
from assertpy import assert_that
from pydantic import parse_raw_as
from requests import Response

from core.api.lms.base import LMSApiObject, LMSApiObjectManager
from core.api.lms.base_api import LmsAsyncApi
from core.models.lms.lms_base import LMSHasKey, LMSMayHasKey
from core.models.lms.objective import Objective
from core.models.lms.reports import ActivityPartReportModel
from core.models.lms.reports import ObjectiveReports as ObjectiveReportsModel
from core.models.query import LoadOptions, QueryResponse
from settings import settings
from util.assertions.common_assertions import assert_response_status


class ObjectiveReportsApi(LmsAsyncApi[ObjectiveReportsModel, LMSMayHasKey, LMSHasKey]):
    NAME = "ObjectiveReports"
    PATH_NAME = "objective-reports"
    URL = f"{settings.base_url_lms_api}{PATH_NAME}"
    MODEL = ObjectiveReportsModel

    def request_get_activity_part_reports_from_objective_report(self, obj_id: str) -> Response:
        return self.session.get(f"{self.get_instance_url(obj_id)}/activity-report")

    def get_activity_part_reports_from_objective_report(
        self, obj_id: str, expected_size: int
    ) -> QueryResponse[ActivityPartReportModel]:
        with allure.step(f"Get activity report from objective report objective ID={obj_id}"):
            response = self.request_get_activity_part_reports_from_objective_report(obj_id)
            assert_response_status(response.status_code, HTTPStatus.OK)

            activity_part_reports = parse_raw_as(QueryResponse[ActivityPartReportModel], response.text)
            assert_that(activity_part_reports.data).is_length(expected_size)

            return activity_part_reports


class ObjectiveReport(LMSApiObject[ObjectiveReportsModel, ObjectiveReportsApi]):
    API = ObjectiveReportsApi


class ObjectiveReportsManager(LMSApiObjectManager[ObjectiveReportsApi, ObjectiveReport]):
    API = ObjectiveReportsApi
    OBJECT = ObjectiveReport

    def get_objective_report(self, objective: Objective) -> ObjectiveReportsModel:
        with allure.step(f"Get objective report objective name={objective.data.name}"):
            reports = self._api.query(LoadOptions(filter=f'["objective.name","=","{objective.data.name}"]'))
            assert_that(reports.data).is_length(1)
            return reports.data[0]
