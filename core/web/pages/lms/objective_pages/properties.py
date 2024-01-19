from selene import browser

from core.web.pages.platform_base_page import PlatformBaseDynamicPage
from util.web.assist.selene.extended import by


class PropertiesPage(PlatformBaseDynamicPage):
    def __init__(self):
        super().__init__(
            url_template="teach/objectives/wizard/{objective_id}/form",
        )

        self.image_info = browser.element(by.class_starts_with("ImageInfo-module_info"))
