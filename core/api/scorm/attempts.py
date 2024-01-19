from http import HTTPStatus

import allure
from requests import Response

from core.api.base_api import ObjectApi, prepare_body
from core.models.scorm.attempts import CreateExitAttempt
from settings import settings
from util.assertions.common_assertions import assert_response_status


class AttemptsApi(ObjectApi):
    NAME = "Attempts"
    PATH_NAME = "attempts"
    URL = f"{settings.base_url_scorm}v1/{PATH_NAME}"

    def request_exit_attempts(self, payload, resource_launch_id: str, activity_workflow_id: str) -> Response:
        url = f"{self.URL}/{activity_workflow_id}/exit"
        return self.session.post(
            url,
            data=prepare_body(payload),
            headers={"Content-type": "application/json"},
            params={"resourceLaunchId": resource_launch_id},
        )

    def exit_attempts(self, payload: CreateExitAttempt, resource_launch_id: str, activity_workflow_id: str):
        with allure.step(f"Exit attempts for resource launch = {resource_launch_id}"):
            response = self.request_exit_attempts(payload, resource_launch_id, activity_workflow_id)
            assert_response_status(response.status_code, HTTPStatus.NO_CONTENT)
