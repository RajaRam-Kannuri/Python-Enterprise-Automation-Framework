from enum import StrEnum
from http import HTTPStatus
from typing import ClassVar, Generic

import allure
from pydantic import parse_raw_as
from requests import Response
from waiting import wait
from waiting.exceptions import TimeoutExpired

from core.api.base_api import (
    ApiModel,
    CreateApiModel,
    ObjectCreatableApi,
    ObjectDeleteableApi,
    ObjectGettableApi,
    ObjectQueryableApi,
    ObjectUpdateableApi,
    UpdateApiModel,
    check_response,
    prepare_body,
)
from core.models.lms.command import Command, Operation
from core.models.lms.lms_base import LMSModelBase
from settings import settings
from util.assertions.common_assertions import assert_response_status


class CommandType(StrEnum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"


class CommandException(Exception):
    def __init__(self, command: Command):
        self.command = command


class CommandFailed(CommandException):
    pass


class CommandTimeouted(CommandException):
    pass


class LmsAsyncApi(
    ObjectGettableApi[ApiModel],
    ObjectCreatableApi[CreateApiModel, ApiModel],
    ObjectDeleteableApi,
    ObjectUpdateableApi[UpdateApiModel, ApiModel],
    ObjectQueryableApi[ApiModel],
    Generic[ApiModel, CreateApiModel, UpdateApiModel],
):
    PATH_NAME: ClassVar[str] = ""

    def post(self, create_data: CreateApiModel) -> ApiModel:
        response = self.request_post(create_data)
        command = self._process_async_response(response, CommandType.CREATE)

        return self.get(command.entity_id)

    def put(self, obj_id: str, data: UpdateApiModel) -> ApiModel:
        response = self.request_put(obj_id, data)
        command = self._process_async_response(response, CommandType.UPDATE)

        return self.get(command.entity_id)

    def delete(self, obj_id: str):
        response = self.request_delete(obj_id)
        self._process_async_response(response, CommandType.DELETE)

    def request_get_cmd(self, cmd_type: CommandType, cmd_id: str) -> Response:
        url = f"{settings.base_url_lms_api}{cmd_type}-{self.PATH_NAME}/{cmd_id}"
        return self.session.get(url)

    def request_list_cmd(self, cmd_type: CommandType) -> Response:
        url = f"{settings.base_url_lms_api}{cmd_type}-{self.PATH_NAME}"
        return self.session.get(url)

    def get_cmd(self, cmd_type: CommandType, cmd_id: str) -> Command:
        with allure.step(f"Get {self.PATH_NAME} command with id {cmd_id}"):
            response = self.request_get_cmd(cmd_type, cmd_id)
            assert_response_status(response.status_code, HTTPStatus.OK)

            return parse_raw_as(Command, response.text)

    def list_cmd(self, cmd_type: CommandType) -> list[Command]:
        with allure.step(f"Get all {self.PATH_NAME} commands"):
            response = self.request_list_cmd(cmd_type)
            assert_response_status(response.status_code, HTTPStatus.OK)

            return parse_raw_as(list[Command], response.text)

    def wait_for_operation(self, operation: Operation) -> Command:
        with allure.step(f"Waiting for opearion {operation.id} to finish"):
            command = self._wait_for_completion(operation.url)

            if not command.is_succeeded():
                raise CommandFailed(command)

            return command

    def wait_for_command(self, command: Command, cmd_type: CommandType) -> Command:
        with allure.step(f"Waiting for command {command.id} to finish"):
            url = f"{settings.base_url_lms_api}{cmd_type}-{self.PATH_NAME}/{command.id}"

            try:
                command = self._wait_for_completion(url)
            except TimeoutExpired:
                raise CommandTimeouted(command)

            if not command.is_succeeded():
                raise CommandFailed(command)

            return command

    def _wait_for_completion(self, url: str) -> Command:
        def wait_condition():
            response = self.session.get(url)
            assert_response_status(response.status_code, HTTPStatus.OK)

            command = parse_raw_as(Command, response.text)

            return command if command.is_completed() else None

        return wait(
            lambda: wait_condition(),
            timeout_seconds=settings.default_command_timeout,
            sleep_seconds=settings.default_command_sleep,
            waiting_for=f"Command {url} to finish",
        )

    def _send_async_request(self, url: str, payload: LMSModelBase) -> Command:
        response = self.session.post(
            url=url,
            data=prepare_body(payload),
            headers={"prefer": "respond-async", "Content-type": "application/json"},
        )
        check_response(response, HTTPStatus.ACCEPTED)

        # Workaround: operation returns url scheme behind api gateway
        # See https://youtrack.constr.dev/issue/ALMS-4371 for more information
        operation = Operation.parse_raw(response.text)
        operation_url = f"{url}/{operation.id}"
        return self._wait_for_completion(operation_url)

    def _process_async_response(self, response: Response, command_type: CommandType) -> Command:
        check_response(response, HTTPStatus.ACCEPTED)

        operation = Operation.parse_raw(response.text)

        command = self.get_cmd(cmd_type=command_type, cmd_id=operation.url.split("/")[-1])
        return self.wait_for_command(command, command_type)
