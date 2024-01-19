from selene import browser

from core.web.pages.platform_base_page import PlatformBaseDynamicPage


class LibraryPageBase(PlatformBaseDynamicPage):
    def __init__(self):
        super().__init__(url_template="teach/content-libraries/{library_id}")
        self.error_message = browser.element(".dx-error-message")
        self.header_row = browser.element("//*[contains(@class,'dx-datagrid-headers')]//tr[@role='row']")
