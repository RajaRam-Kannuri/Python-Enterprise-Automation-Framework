from __future__ import annotations

import allure
from requests import Response

from core.api.base_api import prepare_body
from core.api.lms.activity import Activity
from core.api.lms.base import LMSApiObject, LMSApiObjectManager
from core.api.lms.base_api import LmsAsyncApi
from core.models.lms.activity_part import ActivityPart as ActivityPartModel
from core.models.lms.activity_part import (
    ControlFlowGate,
    CreateActivityPart,
    CreateActivityPartFromResource,
    UpdateActivityPart,
)
from core.models.lms.resource_library import Resource, ResourceLibrary
from settings import settings


class ActivityPartApi(LmsAsyncApi[ActivityPartModel, CreateActivityPart, UpdateActivityPart]):
    NAME = "ActivityPart"
    PATH_NAME = "activity-parts"
    URL = f"{settings.base_url_lms_api}{PATH_NAME}"
    MODEL = ActivityPartModel

    def create_from_resource(self, payload: CreateActivityPartFromResource) -> Response:
        return self.session.post(
            url=f"{self.URL}/from-resource",
            data=prepare_body(payload),
            headers={"Content-type": "application/json"},
        )


class ActivityPart(LMSApiObject[ActivityPartModel, ActivityPartApi]):
    API = ActivityPartApi

    @property
    def activity(self) -> Activity:
        return Activity(self.session, self.data.child_activity)

    def move(self, order: int) -> ActivityPart:
        with allure.step(f"Move activity part {self.data.child_activity.name} to {order} position"):
            return self.put(
                UpdateActivityPart(
                    child_activity=self.data.child_activity, child_activity_id=self.data.child_activity_id, order=order
                )
            )


class ActivityPartManager(LMSApiObjectManager[ActivityPartApi, ActivityPart]):
    API = ActivityPartApi
    OBJECT = ActivityPart

    def __init__(self, parent_activity: Activity):
        super().__init__(parent_activity.session)
        self.parent_activity = parent_activity

    def add_part(
        self,
        child_activity: Activity,
        order: int = 0,
        allowed_attempts: int | None = None,
        score_weight: int = 1,
        progress_weight: float = 1.0,
        gate: ControlFlowGate = ControlFlowGate.FREE,
    ) -> ActivityPart:
        create_data = CreateActivityPart(
            parent_activity_id=self.parent_activity.id,
            child_activity_id=child_activity.id,
            order=order,
            score_weight=score_weight,
            gate=gate,
            allowed_attempts=allowed_attempts,
            progress_weight=progress_weight,
        )

        with allure.step(f"Add {child_activity.data.name} to composite {self.parent_activity.data.name}"):
            data = self._api.post(create_data)
            return ActivityPart(self.session, data)

    def add_scorm_part(
        self,
        resource: Resource,
        resource_library: ResourceLibrary,
        team_id: str,
        order: int,
        allowed_attempts: int | None = None,
        progress_weight: int | None = 1.0,
        gate: ControlFlowGate = ControlFlowGate.FREE,
    ) -> ActivityPart:
        create_data = CreateActivityPartFromResource(
            parent_activity_id=self.parent_activity.id,
            resource_id=resource.id,
            resource_library_id=resource_library.id,
            order=order,
            allowed_attempts=allowed_attempts,
            gate=gate,
            team_id=team_id,
            progress_weight=progress_weight,
        )

        with allure.step(f"Add {resource.name} to composite {self.parent_activity.data.name}"):
            data = self._api.create_from_resource(create_data)
            return ActivityPart(self.session, data)
