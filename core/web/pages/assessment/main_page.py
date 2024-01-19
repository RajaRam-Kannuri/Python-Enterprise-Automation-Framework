from core.web.pages.platform_base_page import PlatformBaseStaticPage
from settings import settings


class MainAssessmentPage(PlatformBaseStaticPage):
    URL = settings.base_url_assessment_ui

    def __init__(self):
        super().__init__(url=self.URL)
