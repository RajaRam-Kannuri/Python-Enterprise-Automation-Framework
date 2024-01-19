import re

from selene import browser, by, have

from core.web.pages.platform_base_page import PlatformBaseDynamicPage


class BasePreviewPage(PlatformBaseDynamicPage):
    def __init__(self, url_template):
        super().__init__(url_template=url_template)
        self.continue_lab_button = browser.element(by.text("Continue the lab"))

    def get_session_id_from_url(self):
        """Parse url for a session id"""
        browser.should(have.url_containing("session_id="))
        parsed_url = re.search(r".*session_id=(?P<session_id>.*)", browser.driver.current_url)
        return parsed_url.group("session_id")
