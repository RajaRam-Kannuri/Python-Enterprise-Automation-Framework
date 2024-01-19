from __future__ import annotations

import json
import typing
from functools import cached_property
from http import HTTPStatus
from time import time

import allure
from pydantic import parse_raw_as
from requests import Response

from core.api.lms.base import LMSApiObject, LMSApiObjectManager, LmsAsyncApi
from core.api.lms.resource_library import ResourceLibrary
from core.models.lms.activity import Activity as ActivityModel
from core.models.lms.activity import ActivityState, ActivityType, CreateActivity, LtiVersion, UpdateActivity
from core.models.lms.activity_part import ActivityPart as ActivityPartModel
from core.models.lms.resource_library import Resource
from core.models.lms.resource_library import ResourceLibrary as ResourceLibraryModel
from core.models.lms.resource_library import ResourceLibraryType
from core.models.scorm.organization import Organization
from settings import settings
from util.assertions.common_assertions import assert_response_status

if typing.TYPE_CHECKING:
    from core.api.lms.activity_part import ActivityPart, ActivityPartManager


class ActivityApi(LmsAsyncApi[ActivityModel, CreateActivity, UpdateActivity]):
    NAME = "Activity"
    PATH_NAME = "activities"
    URL = f"{settings.base_url_lms_api}{PATH_NAME}"
    MODEL = ActivityModel

    def request_get_parts(self, obj_id: str) -> Response:
        return self.session.get(f"{self.get_instance_url(obj_id)}/activity-parts")

    def get_parts(self, obj_id: str) -> list[ActivityPartModel]:
        with allure.step(f"Get activity {obj_id} parts"):
            response = self.request_get_parts(obj_id)
            assert_response_status(response.status_code, HTTPStatus.OK)

            return parse_raw_as(list[ActivityPartModel], response.text)


class Activity(LMSApiObject[ActivityModel, ActivityApi]):
    API = ActivityApi

    def set_state(self, state: ActivityState):
        with allure.step(f"Set activity {self.data.name} {self.id} state to {state.name}"):
            # TODO: There is an issue on backend - for now we should pass all fields in update request
            # See for more info: https://youtrack.constr.dev/issue/ALMS-3752
            update_data = UpdateActivity(**self.data.dict(exclude={"id"}))
            update_data.state = state

            self.put(update_data)


class RichTextActivity(Activity):
    def set_content(self, paragraphs: str | list[str]):
        with allure.step(f"Set content for activity {self.data.name}"):
            # UI uses codex editor - https://codex.so/editor
            # Set content in the format to be visible in UI
            # Now support only several paragraphs, more sophisticated content - to add later
            if isinstance(paragraphs, str):
                paragraphs = [paragraphs]

            update_data = UpdateActivity(**self.data.dict(exclude={"id"}))
            update_data.content = "".join(f'<p class="paragraph left">{p}<p>' for p in paragraphs)
            update_data.editor_content = json.dumps(
                {
                    "time": int(time() * 1000),
                    "blocks": [{"type": "paragraph", "data": {"text": p, "alignment": "left"}} for p in paragraphs],
                    "version": "2.23.2",
                }
            )

            self.put(update_data)


class CompositeActivity(Activity):
    def get_parts(self) -> list[ActivityPartModel]:
        return self._api.get_parts(self.id)

    @cached_property
    def parts_manager(self) -> ActivityPartManager:
        from core.api.lms.activity_part import ActivityPartManager

        return ActivityPartManager(self)

    @cached_property
    def parts(self) -> list[ActivityPart]:
        from core.api.lms.activity_part import ActivityPart

        return [ActivityPart(self.session, data) for data in self.get_parts()]

    def invalidate_parts(self):
        if "parts" in self.__dict__:
            self.__dict__.pop("parts")

    def add_part(self, child_activity: Activity, order=0, allowed_attempts=None) -> ActivityPart:
        self.invalidate_parts()
        return self.parts_manager.add_part(child_activity, order, allowed_attempts)

    def remove_part(self, part: ActivityPart):
        if part.id not in {p.id for p in self.parts}:
            raise RuntimeError(f"Part {part.data.id} is not in composition")
        self.invalidate_parts()
        part.delete()

    def move_part(self, part: ActivityPart, order: int):
        if part.id not in {p.id for p in self.parts}:
            raise RuntimeError(f"Part {part.data.id} is not in composition")
        self.invalidate_parts()

        part.move(order)

    def add_scorm_part(
        self, resource: Resource, resource_library: ResourceLibraryModel, team_id: str, order=0, allowed_attempts=None
    ) -> ActivityPart:
        self.invalidate_parts()
        return self.parts_manager.add_scorm_part(resource, resource_library, team_id, order, allowed_attempts)


class ActivityManager(LMSApiObjectManager[ActivityApi, Activity]):
    API = ActivityApi
    OBJECT = Activity

    def create_with_library(self, resource_library: ResourceLibraryModel) -> RichTextActivity | CompositeActivity:
        if resource_library.type == ResourceLibraryType.Text:
            activity_type = ActivityType.TEXT
            activity_class = RichTextActivity
        elif resource_library.type == ResourceLibraryType.Composite:
            activity_type = ActivityType.COMPOSITE
            activity_class = CompositeActivity
        else:
            raise RuntimeError(f"Unknown activity type for {resource_library.name} library")

        with allure.step(f"Create {activity_type.name} activity in {resource_library} library"):
            create_data = CreateActivity(
                type=activity_type,
                resource_library_id=resource_library.id,
                state=ActivityState.DRAFT,
            )

            data = self._api.post(create_data)
            return activity_class(self._api.session, data)

    def create_from_organization(self, resource_library: ResourceLibrary, organization: Organization) -> Activity:
        create_data = CreateActivity(
            code=organization.data.code,
            name=organization.data.title,
            type=ActivityType.LTI,
            resource_library_id=resource_library.id,
            tool_url=f"{resource_library.lti_form.target_link_uri}/{organization.data.id}",
            lti_version=LtiVersion.LTI13,
            tool_resource_id=organization.data.id,
            state=ActivityState.READY,
            support_lti_grading=True,
            support_lti_authoring=True,
            tool_auth_url=resource_library.lti_form.auth_uri,
        )
        with allure.step(f"Create scorm activity from organization {organization.data.code}"):
            data = self._api.post(create_data)
            return Activity(self._api.session, data)
