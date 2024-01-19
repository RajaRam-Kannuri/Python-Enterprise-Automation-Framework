import allure
from selene import browser

from core.web.pages.platform_base_page import PlatformBaseStaticPage
from util.web.assist.allure import report
from util.web.assist.selene.extended import by


class ContentLibraryPage(PlatformBaseStaticPage):
    URL = "teach/content-libraries/"

    def __init__(self):
        super().__init__(self.URL)
        self.scorm_library = browser.element("//a[div[contains(text(),'SCORM')]]")
        self.library_elements = browser.all(by.class_contains("resourceLibraryName"))

    @report.step
    def open_library(self, library_name):
        with allure.step(f"Open '{library_name}' library on content page"):
            library_element = browser.element(f"//a[div[contains(text(),'{library_name}')]]")
            library_element.click()
        return self
