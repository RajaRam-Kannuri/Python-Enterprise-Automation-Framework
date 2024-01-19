from functools import cached_property
from typing import Self

import allure
import requests
from requests import Session

from core.api.base_refactored.api_client import ApiClient, ManagerApiClient, SingleItemApiClient
from core.api.labs.base import LabsCommonManager, LabsCommonObjectWrapper
from core.api.labs.lab import LabWrapper
from core.models.labs.task import LabsTaskLinkInputModel, LabsTaskLinkModel, TranslatedTask, TranslatedTaskInput
from settings import settings


class TaskClient(SingleItemApiClient):
    URL_TEMPLATE = f"{settings.base_url_labs}api/labs/tasks/{{id}}/"
    NAME = "task"

    def request_clone(self) -> requests.Response:
        with allure.step(f'Cloning task with id "{self.id}"'):
            response = self.api_session.post(url=f"{self.url}clone/")
            return response

    def request_approve_translations(self, data: dict) -> requests.Response:
        with allure.step(f"Approve translations in {self}"):
            response = self.api_session.post(url=f"{self.url}approve_translations/", json=data)
            return response


class TaskWrapper(LabsCommonObjectWrapper[TaskClient, TranslatedTask, TranslatedTaskInput]):
    API_CLASS = TaskClient
    DATA_MODEL = TranslatedTask
    INPUT_CLASS_MODEL = TranslatedTaskInput

    def clone(self) -> Self:
        response = self.api.request_clone()
        response.raise_for_status()
        return TaskWrapper(api_session=self.api_session, data=response.json())


class LabTaskLinkClient(SingleItemApiClient):
    URL_TEMPLATE = f"{settings.base_url_labs}api/labs/{{lab_id}}/tasks/{{id}}/"
    NAME = "task in a lab"

    def __init__(self, api_session: Session, related_lab_id: str, object_id: str):
        super().__init__(api_session, object_id)
        self.related_lab_id = related_lab_id

    def __str__(self) -> str:
        return f"{self.NAME} with id {self.id} in a lab with id {self.related_lab_id}"

    @cached_property
    def url(self):
        return self.URL_TEMPLATE.format(id=self.id, lab_id=self.related_lab_id)

    def request_move(self, index: int) -> requests.Response:
        with allure.step(f'Moving {self} to "{index}" place'):
            response = self.api_session.post(url=f"{self.url}move/", json={"order": index})
            return response


class LabTaskLinkWrapper(LabsCommonObjectWrapper[LabTaskLinkClient, LabsTaskLinkModel, LabsTaskLinkInputModel]):
    API_CLASS = LabTaskLinkClient
    DATA_MODEL = LabsTaskLinkModel
    INPUT_CLASS_MODEL = LabsTaskLinkInputModel

    def __init__(
        self,
        api_session: Session,
        data: dict | LabsTaskLinkModel,
        related_lab_id: str,
        related_task: TaskWrapper | None = None,
    ):
        data: LabsTaskLinkModel = self.DATA_MODEL(**data) if isinstance(data, dict) else data
        super().__init__(
            api_session,
            data,
            api=LabTaskLinkClient(api_session=api_session, object_id=data.id, related_lab_id=related_lab_id),
        )
        self.related_lab_id = related_lab_id
        self._related_task = related_task
        self.api: LabTaskLinkClient = self.API_CLASS(
            api_session=api_session, object_id=self.id, related_lab_id=related_lab_id
        )

    @cached_property
    def steps_manager(self):
        from core.api.labs.step import StepsInTaskManager

        return StepsInTaskManager(self)

    @property
    def task_object(self) -> TaskWrapper:
        if self._related_task is None:
            self._related_task = TaskWrapper(api_session=self.api_session, object_id=self.id)
        return self._related_task

    def move_to_index(self, index: int) -> requests.Response:
        response = self.api.request_move(index)
        response.raise_for_status()
        self._update_inner_data(response)
        return response


class TasksManagerClient(ManagerApiClient):
    URL = f"{settings.base_url_labs}api/labs/tasks/"


class TasksManager(LabsCommonManager[TasksManagerClient, TaskWrapper, TranslatedTaskInput]):
    API_CLASS = TasksManagerClient
    CREATE_MODEL = TranslatedTaskInput
    SINGLE_OBJECT_CLASS = TaskWrapper

    def create_task(self, input_data_model: TranslatedTaskInput | None = None) -> TaskWrapper:
        return self.create(input_data_model or TranslatedTaskInput())

    def create_task_with_name(self, task_name: str) -> TaskWrapper:
        return self.create(TranslatedTaskInput(name=task_name))


class TasksInLabManagerClient(ApiClient):
    URL_TEMPLATE = f"{settings.base_url_labs}api/labs/{{lab_id}}/tasks/"
    NAME = "tasks in a lab"

    def __init__(self, api_session, lab_id):
        super().__init__(api_session)
        self.lab_id = lab_id

    @cached_property
    def url(self) -> str:
        return self.URL_TEMPLATE.format(lab_id=self.lab_id)

    def request_attach_task_to_lab(self, task_id) -> requests.Response:
        response = self.api_session.post(url=f"{self.url}{task_id}/")
        return response

    def request_query(self, params: dict | None = None) -> requests.Response:
        with allure.step(f"getting tasks in a lab {self.lab_id} with data {params}"):
            response = self.api_session.get(self.url, params=params)
            return response

    def request_reorder(self, data) -> requests.Response:
        response = self.api_session.post(url=f"{self.url}reorder/", json=data)
        return response


class TasksInLabManager:
    def __init__(self, lab: LabWrapper):
        self.url = f"{settings.base_url_labs}api/labs/{lab.id}/tasks/"
        self.api: TasksInLabManagerClient = TasksInLabManagerClient(api_session=lab.api_session, lab_id=lab.id)
        self.latest_response: requests.Response | None = None
        self.lab_id = lab.id
        self._tasks_local_data: list[LabsTaskLinkModel] = [
            LabsTaskLinkModel.construct(id=task) for task in lab.data.tasks
        ]
        self.previous_tasks_data: list[LabsTaskLinkModel] | None = None
        self._local_data_is_valid: bool = True

    @property
    def api_session(self):
        return self.api.api_session

    def _update_inner_data(self, response: requests.Response):
        self.latest_response = response
        self.previous_tasks_data = self._tasks_local_data
        self._tasks_local_data = [LabsTaskLinkModel(**obj) for obj in response.json()]

    def _invalidate_local_data(self):
        self._local_data_is_valid = False

    @property
    def tasks_local_data(self) -> list[LabsTaskLinkModel]:
        if self._local_data_is_valid:
            return self._tasks_local_data
        self.fetch_data()
        self._local_data_is_valid = True
        return self._tasks_local_data

    def fetch_data(self) -> requests.Response:
        response = self.api.request_query()
        response.raise_for_status()
        self._update_inner_data(response)
        return response

    def add_task(self, task: TaskWrapper) -> LabTaskLinkWrapper:
        response = self.api.request_attach_task_to_lab(task.id)
        response.raise_for_status()
        self._invalidate_local_data()
        return LabTaskLinkWrapper(
            api_session=self.api_session, data=response.json(), related_lab_id=self.lab_id, related_task=task
        )

    @property
    def tasks(self) -> list[LabTaskLinkWrapper]:
        return [
            LabTaskLinkWrapper(api_session=self.api_session, data=task, related_lab_id=self.lab_id)
            for task in self.tasks_local_data
        ]
