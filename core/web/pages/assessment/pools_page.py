from urllib.parse import urljoin

from core.web.pages.platform_base_page import PlatformBaseStaticPage
from settings import settings


class PoolsPage(PlatformBaseStaticPage):
    URL = urljoin(settings.base_url_assessment_ui, "pools")

    def __init__(self):
        super().__init__(url=self.URL)
