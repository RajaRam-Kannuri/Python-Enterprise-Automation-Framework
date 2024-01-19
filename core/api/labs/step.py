from functools import cached_property
from typing import List, Self

import allure
import requests
from requests import Session

from core.api.base_refactored.api_client import ApiClient, ManagerApiClient, SingleItemApiClient
from core.api.labs.base import LabsCommonManager, LabsCommonObjectWrapper
from core.api.labs.criteria import CriteriaWrapper
from core.api.labs.task import LabTaskLinkWrapper, TaskWrapper
from core.models.labs.step import StepInput, StepModel, TaskStepLinkModel, TaskStepLinkRequestModel
from settings import settings


class StepClient(SingleItemApiClient):
    NAME = "step"
    URL_TEMPLATE = f"{settings.base_url_labs}api/labs/tasks/steps/{{id}}/"

    def request_clone(self) -> requests.Response:
        with allure.step(f'Cloning task with id "{self.id}"'):
            response = self.api_session.post(url=self.url + "clone/")
            return response


class StepWrapper(LabsCommonObjectWrapper[StepClient, StepModel, StepInput]):
    API_CLASS = StepClient
    DATA_MODEL = StepModel
    INPUT_CLASS_MODEL = StepInput

    @property
    def acceptance_criteria(self) -> List[CriteriaWrapper]:
        result = [
            CriteriaWrapper(api_session=self.api_session, data=criteria) for criteria in self.data.acceptance_criteria
        ]
        return result

    def clone(self) -> Self:
        response = self.api.request_clone()
        response.raise_for_status()
        return StepWrapper(api_session=self.api_session, data=response.json())


class TaskStepLinkClient(SingleItemApiClient):
    URL_TEMPLATE = f"{settings.base_url_labs}api/labs/tasks/{{task_id}}/steps/{{id}}/"
    NAME = "task step link"

    def __init__(
        self,
        api_session: Session,
        related_task_id: str,
        object_id: str,
    ):
        super().__init__(api_session, object_id)
        self.related_task_id = related_task_id

    def __str__(self) -> str:
        return f"{self.NAME} with id {self.id} in a task with id {self.related_task_id}"

    @cached_property
    def url(self):
        return self.URL_TEMPLATE.format(id=self.id, task_id=self.related_task_id)

    def request_move(self, index: int) -> requests.Response:
        with allure.step(f'Moving {self} to "{index}" place'):
            response = self.api_session.post(url=f"{self.url}move/", json={"order": index})
            return response


class TaskStepLinkWrapper(LabsCommonObjectWrapper[TaskStepLinkClient, TaskStepLinkModel, TaskStepLinkRequestModel]):
    API_CLASS = TaskStepLinkClient
    DATA_MODEL = TaskStepLinkModel
    INPUT_CLASS_MODEL = TaskStepLinkRequestModel

    def __init__(
        self,
        api_session: Session,
        data: dict | TaskStepLinkModel,
        related_task_id: str,
        related_step: StepWrapper | None = None,
    ):
        data: TaskStepLinkModel = self.DATA_MODEL(**data) if isinstance(data, dict) else data
        super().__init__(
            api_session=api_session,
            data=data,
            api=TaskStepLinkClient(api_session=api_session, object_id=data.id, related_task_id=related_task_id),
        )
        self.related_task_id = related_task_id
        self._related_step = related_step

    @property
    def acceptance_criteria(self) -> List[CriteriaWrapper]:
        result = [
            CriteriaWrapper(api_session=self.api_session, data=criteria) for criteria in self.data.acceptance_criteria
        ]
        return result

    @property
    def step_object(self) -> StepWrapper:
        if self._related_step is None:
            self._related_step = StepWrapper(api_session=self.api_session, data=StepModel.construct(id=self.id))
        return self._related_step


class StepsManagerClient(ManagerApiClient):
    URL = f"{settings.base_url_labs}api/labs/tasks/steps/"


class StepsManager(LabsCommonManager[StepsManagerClient, StepWrapper, StepInput]):
    API_CLASS = StepsManagerClient
    SINGLE_OBJECT_CLASS = StepWrapper
    CREATE_MODEL = StepInput

    def create_step(self, input_data_model: StepInput | None = None) -> StepWrapper:
        return self.create(input_data_model or StepInput())

    def create_step_with_name(self, step_name: str) -> StepWrapper:
        return self.create(StepInput(name=step_name))


class StepsInTaskManagerClient(ApiClient):
    URL_TEMPLATE = f"{settings.base_url_labs}api/labs/tasks/{{task_id}}/steps/"
    NAME = "steps in a task"

    def __init__(self, api_session, task_id):
        super().__init__(api_session)
        self.task_id = task_id

    @cached_property
    def url(self):
        return self.URL_TEMPLATE.format(task_id=self.task_id)

    def request_attach_step_to_task(self, step_id) -> requests.Response:
        response = self.api_session.post(url=f"{self.url}{step_id}/")
        return response

    def request_query(self, params: dict | None = None) -> requests.Response:
        with allure.step(f"getting steps in a task {self.task_id} with data {params}"):
            response = self.api_session.get(self.url, params=params)
            return response

    def request_reorder(self, data) -> requests.Response:
        response = self.api_session.post(url=self.url + "reorder/", json=data)
        return response


class StepsInTaskManager:
    def __init__(self, task: TaskWrapper | LabTaskLinkWrapper):
        self.task_id = task.id
        self.url = f"{settings.base_url_labs}api/labs/tasks/{self.task_id}/steps/"
        self.api: StepsInTaskManagerClient = StepsInTaskManagerClient(
            api_session=task.api_session, task_id=self.task_id
        )
        self._steps_local_data: List[TaskStepLinkModel] = [
            TaskStepLinkModel.construct(id=step, task=task.id) for step in task.data.steps
        ]
        self.previous_steps_data: list[TaskStepLinkModel] | None = None
        self._local_data_is_valid: bool = True

    @property
    def api_session(self):
        return self.api.api_session

    def _update_inner_data(self, response: requests.Response):
        self.latest_response = response
        self.previous_tasks_data = self._steps_local_data
        self._tasks_local_data = [TaskStepLinkModel(**obj) for obj in response.json()]

    def _invalidate_local_data(self):
        self._local_data_is_valid = False

    @property
    def steps_local_data(self):
        if self._local_data_is_valid:
            return self._steps_local_data
        self.fetch_data()
        self._local_data_is_valid = True
        return self._steps_local_data

    def fetch_data(self) -> requests.Response:
        response = self.api.request_query()
        response.raise_for_status()
        self._update_inner_data(response)
        return response

    def add_step(self, step: StepWrapper) -> TaskStepLinkWrapper:
        response = self.api.request_attach_step_to_task(step.id)
        response.raise_for_status()
        self._steps_local_data.append(response.json())
        return TaskStepLinkWrapper(
            api_session=self.api_session, data=response.json(), related_task_id=self.task_id, related_step=step
        )

    @property
    def steps(self):
        return [
            TaskStepLinkWrapper(api_session=self.api_session, data=step, related_task_id=self.task_id)
            for step in self.steps_local_data
        ]
