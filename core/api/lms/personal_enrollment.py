from datetime import UTC, datetime, timedelta

import allure

from core.api.base_api import ObjectNotFound
from core.api.lms.base import LMSApiObject, LMSApiObjectManager
from core.api.lms.base_api import LmsAsyncApi
from core.models.lms.lms_user import User
from core.models.lms.objective import Objective
from core.models.lms.personal_enrollments import CreatePersonalEnrollment
from core.models.lms.personal_enrollments import PersonalEnrollment as PersonalEnrollmentModel
from core.models.lms.personal_enrollments import UpdatePersonalEnrollment
from settings import settings


class PersonalEnrollmentApi(LmsAsyncApi[PersonalEnrollmentModel, CreatePersonalEnrollment, UpdatePersonalEnrollment]):
    NAME = "PersonalEnrollment"
    PATH_NAME = "personal-enrollments"
    URL = f"{settings.base_url_lms_api}{PATH_NAME}"
    MODEL = PersonalEnrollmentModel


class PersonalEnrollment(LMSApiObject[PersonalEnrollmentModel, PersonalEnrollmentApi]):
    API = PersonalEnrollmentApi

    def teardown(self):
        try:
            self.delete()
        except ObjectNotFound:
            pass


class PersonalEnrollmentManager(LMSApiObjectManager[PersonalEnrollmentApi, PersonalEnrollment]):
    API = PersonalEnrollmentApi
    OBJECT = PersonalEnrollment

    def create(
        self,
        objective: Objective,
        user: User,
        due_date: datetime = datetime.now(UTC) + timedelta(hours=12),
        availability_date: datetime = datetime.now(UTC),
        availability_end_date: datetime = datetime.now(UTC) + timedelta(days=1),
        retake=True,
        mandatory=True,
    ) -> PersonalEnrollment:
        with allure.step(f"Create personal enrollment for user {user.username} to objective {objective.name}"):
            create_data = CreatePersonalEnrollment(
                objective_id=objective.id,
                user_id=user.id,
                due_date=due_date,
                availability_date=availability_date,
                availability_end_date=availability_end_date,
                retake=retake,
                is_mandatory=mandatory,
            )
            data = self._api.post(create_data)
            return PersonalEnrollment(self.session, data)
