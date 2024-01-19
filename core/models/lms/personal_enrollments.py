from datetime import datetime
from enum import IntEnum

from core.models.lms.lms_base import LMSEntityModelBase, LMSModelBase
from core.models.lms.lms_user import User


class GradeRevealPolicy(IntEnum):
    NONE = 0
    NEVER = 1
    AFTER_FINISH = 2
    AFTER_DATE = 3


class PersonalEnrollmentBase(LMSModelBase):
    due_date: datetime | None = None
    availability_date: datetime | None = None
    availability_end_date: datetime | None = None
    retake: bool | None = None
    is_mandatory: bool | None = None
    external_id: str | None = None
    grade_reveal_policy: GradeRevealPolicy = GradeRevealPolicy.AFTER_FINISH
    grade_reveal_date: datetime | None = None


class PersonalEnrollment(LMSEntityModelBase, PersonalEnrollmentBase):
    id: str
    objective_id: str
    user: User


class CreatePersonalEnrollment(PersonalEnrollmentBase):
    objective_id: str
    user_id: str


class UpdatePersonalEnrollment(PersonalEnrollmentBase):
    pass
