from http import HTTPStatus

import allure
from pydantic import parse_raw_as
from requests import Response

from core.api.lms.base import LMSApiObject, LMSApiObjectManager
from core.api.lms.base_api import LmsAsyncApi
from core.models.lms.activity import Activity
from core.models.lms.objective import CreateObjective
from core.models.lms.objective import Objective as ObjectiveModel
from core.models.lms.objective import UpdateObjective
from core.models.lms.personal_enrollments import PersonalEnrollment
from core.models.query import LoadOptions
from settings import settings
from util.assertions.common_assertions import assert_response_status
from util.helpers import first


class ObjectiveApi(LmsAsyncApi[ObjectiveModel, CreateObjective, UpdateObjective]):
    NAME = "Objective"
    PATH_NAME = "objectives"
    URL = f"{settings.base_url_lms_api}{PATH_NAME}"
    MODEL = ObjectiveModel

    def request_get_personal_enrollments(self, obj_id: str) -> Response:
        return self.session.get(f"{self.get_instance_url(obj_id)}/personal-enrollments")

    def get_personal_enrollments(self, obj_id: str) -> list[PersonalEnrollment]:
        with allure.step(f"Get personal enrollments for Objective {obj_id}"):
            response = self.request_get_personal_enrollments(obj_id)
            assert_response_status(response.status_code, HTTPStatus.OK)

            return parse_raw_as(list[PersonalEnrollment], response.text)

    def request_query_personal_enrollments(self, obj_id: str, load_options: LoadOptions) -> Response:
        return self.session.get(
            f"{self.get_instance_url(obj_id)}/personal-enrollments/query", params=load_options.lms_dict()
        )

    def query_personal_enrollments(self, obj_id: str, load_options: LoadOptions):
        with allure.step(f"Query personal enrollments for Objective {obj_id}"):
            response = self.request_query_personal_enrollments(obj_id, load_options)
            assert_response_status(response.status_code, HTTPStatus.OK)

            return parse_raw_as(list[PersonalEnrollment], response.text)


# TODO: group enrollments, org unit enrollments, records, accesses, workflow aggregates


class Objective(LMSApiObject[ObjectiveModel, ObjectiveApi]):
    API = ObjectiveApi

    @property
    def personal_enrollments(self) -> list[PersonalEnrollment]:
        return self._api.get_personal_enrollments(self.id)

    def query_personal_enrollments(self, load_options: LoadOptions) -> list[PersonalEnrollment]:
        return self._api.query_personal_enrollments(self.id, load_options)


class ObjectiveManager(LMSApiObjectManager[ObjectiveApi, Objective]):
    API = ObjectiveApi
    OBJECT = Objective

    def create_from_activity(self, activity: Activity):
        with allure.step(f"Create objective from activity {activity.id}"):
            create_data = CreateObjective(activity_id=activity.id)
            data = self._api.post(create_data)
            return Objective(self.session, data)

    def get_by_code(self, code: str) -> Objective:
        with allure.step(f"Get objective data by code = {code}"):
            load_options = LoadOptions(take=1, filter=f'["code","=","{code}"]')
            query_result = self.query(load_options)
            return first(query_result)
