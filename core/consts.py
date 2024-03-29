# Constants for the application
# Will be the same between all environments
from enum import StrEnum

APPLICATION_ID_COMMON = "00000000-0000-0000-0000-000000000000"
APPLICATION_ID_ASSESSMENT = "735a1002-f789-41b8-a878-b946ee8e73ab"
APPLICATION_ID_LABS = "493d9e21-e3e4-4ada-9e6e-3a689d6fab77"
APPLICATION_ID_LMS_API = "23f0073f-0a50-4ae0-aa16-ee78b4bb0b86"
APPLICATION_ID_PLATFORM_API = "0f8d0b3d-682a-461f-a2ae-22f92cfeeba5"
APPLICATION_ID_IDP = "eb670ac2-bddc-43d3-afc2-ad2b1ff27e01"
APPLICATION_ID_CLASSROOM = "9ba443f8-0f02-441d-9bd7-6bfa3efa0643"
APPLICATION_ID_AVATAR = "10156117-4942-4eae-aca1-45b6f060fca8"
APPLICATION_ID_PROCTOR = "29c61722-20bf-4b7e-a6ef-9857d039cb1d"


class AssessmentPermissions(StrEnum):
    DOMAIN_READ = "Domain.Read"
    DOMAIN_CREATE = "Domain.Create"
    DOMAIN_DELETE = "Domain.Delete"
    DOMAIN_UPDATE = "Domain.Update"
    LMS_CREATE = "LMS.Create"
    LMS_DELETE = "LMS.Delete"
    LMS_READ = "LMS.Read"
    LMS_UPDATE = "LMS.Update"
    LMS_READ_ACTIVITIES = "LMS.Read.Activities"
    MESSAGE_READ = "Message.Read"
    MESSAGE_CREATE = "Message.Create"
    MESSAGE_UPDATE = "Message.Update"
    QUESTION_READ_FILE = "Question.Read.File"
    QUESTION_CREATE = "Question.Create"
    QUESTION_DELETE = "Question.Delete"
    QUESTION_READ = "Question.Read"
    QUESTION_READ_PREVIEW = "Question.Read.Preview"
    QUESTION_UPDATE = "Question.Update"
    TAG_READ = "Tag.Read"
    TAG_CREATE = "Tag.Create"
    TOPIC_QUESTION_READ = "TopicQuestion.Read"
    TOPIC_QUESTION_CREATE = "TopicQuestion.Create"
    QUESTION_POOL_CREATE = "QuestionPool.Create"
    QUESTION_POOL_DELETE = "QuestionPool.Delete"
    QUESTION_POOL_READ = "QuestionPool.Read"
    QUESTION_POOL_UPDATE = "QuestionPool.Update"
    QUIZ_CREATE = "Quiz.Create"
    QUIZ_DELETE = "Quiz.Delete"
    QUIZ_READ = "Quiz.Read"
    QUIZ_READ_PREVIEW = "Quiz.Read.Preview"
    QUIZ_READ_FILE = "Quiz.Read.File"
    QUIZ_UPDATE = "Quiz.Update"
    ASSESSMENT_READ = "Assessment.Read"
    ASSESSMENT_READ_HINTS = "Assessment.Read.Hints"
    ASSESSMENT_CREATE = "Assessment.Create"
    ASSESSMENT_UPDATE_SUBMIT = "Assessment.Update.Submit"
