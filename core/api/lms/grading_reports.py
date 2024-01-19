import allure

from core.api.lms.base import LMSApiObject, LMSApiObjectManager
from core.api.lms.base_api import LmsAsyncApi
from core.models.lms.lms_base import LMSHasKey, LMSMayHasKey
from core.models.lms.reports import GradingReports as GradingReportsModel
from core.models.query import LoadOptions
from settings import settings
from util.helpers import first


class GradingReportsApi(LmsAsyncApi[GradingReportsModel, LMSMayHasKey, LMSHasKey]):
    NAME = "GradingReports"
    PATH_NAME = "for-grading-reports"
    URL = f"{settings.base_url_lms_api}{PATH_NAME}"
    MODEL = GradingReportsModel


class GradingReport(LMSApiObject[GradingReportsModel, GradingReportsApi]):
    API = GradingReportsApi


class GradingReportsManager(LMSApiObjectManager[GradingReportsApi, GradingReport]):
    API = GradingReportsApi
    OBJECT = GradingReport

    def get_by_activity_name(self, activity_name: str) -> GradingReport | None:
        with allure.step(f"Get grading report with activity name: {activity_name}"):
            load_options = LoadOptions(take=1, filter=f'["activity.name","=","{activity_name}"]')
            query_result = self.query(load_options)
            return first(query_result)
