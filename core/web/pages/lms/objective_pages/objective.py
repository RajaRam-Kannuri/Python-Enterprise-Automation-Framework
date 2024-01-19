from selene import browser

from core.web.pages.platform_base_page import PlatformBaseDynamicPage, SideMenu
from util.web.assist.allure import report


class ObjectivePage(PlatformBaseDynamicPage):
    def __init__(self):
        super().__init__(
            url_template="teach/objectives/wizard/{objective_id}/info",
        )
        self.side_menu = SideMenu()

    @report.step
    def open_objective_preview_by_id(self, objective_id: str):
        objective_url = f"teach/objectives/wizard/{objective_id}/info?preview=true"
        browser.open(objective_url)
        return self
