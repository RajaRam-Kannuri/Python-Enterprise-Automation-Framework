from urllib.parse import urljoin

from core.web.pages.platform_base_page import PlatformBaseStaticPage
from settings import settings


class QuizzesPage(PlatformBaseStaticPage):
    URL = urljoin(settings.base_url_assessment_ui, "quizzes")

    def __init__(self):
        super().__init__(self.URL)
