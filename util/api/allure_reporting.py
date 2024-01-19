import json
from collections.abc import Mapping

import allure
from allure_commons.types import AttachmentType
from requests import PreparedRequest, Response


def prettify_dict(value: Mapping) -> str:
    """
    Print neat human-readable json from dict
    """
    return json.dumps(value, indent=4)


def attach_request_data(request: PreparedRequest):
    with allure.step("Request"):
        allure.attach(request.url, name="url", attachment_type=AttachmentType.URI_LIST)
        allure.attach(prettify_dict(dict(request.headers)), name="headers", attachment_type=AttachmentType.JSON)

        if "application/json" in request.headers.get("content-type", ""):
            allure.attach(prettify_dict(json.loads(request.body)), name="json", attachment_type=AttachmentType.JSON)
        elif request.body:
            allure.attach(request.body, name="body")


def attach_response_data(response: Response):
    with allure.step("Response"):
        allure.attach(str(response.status_code), name="status code")
        allure.attach(prettify_dict(dict(response.headers)), name="headers", attachment_type=AttachmentType.JSON)

        if "application/json" in response.headers.get("content-type", ""):
            allure.attach(prettify_dict(response.json()), name="json", attachment_type=AttachmentType.JSON)
        elif response.text:
            allure.attach(response.text, name="text")


def record_response(response: Response, *args, **kwargs):
    request = response.request

    with allure.step(f"API call {response.request.method}"):
        attach_request_data(request)
        attach_response_data(response)
