import allure
from selene import be, browser, have

from core.web.pages.platform_base_page import PlatformBaseStaticPage
from settings import settings
from util.web.assist.allure import report


class MyCoursesPage(PlatformBaseStaticPage):
    URL = "learn/courses"

    def __init__(self):
        super().__init__(self.URL)
        self.spinner = browser.element('//*[@data-testid="spinner"]')
        self.course_cards = browser.all("//a[contains(@class,'Course')]")

    @report.step
    def open_course_by_title(self, course_title):
        with allure.step(f"Open '{course_title}'"):
            if not self.course_cards.filtered_by(have.text(course_title)).wait_until(have.size(1)):
                self.refresh()
            course_element = self.course_cards.element_by(have.text(course_title))
            course_element.click()

        return self

    @report.step
    def wait_for_spinner_to_hide(self):
        if self.spinner.with_(timeout=settings.recheck_timeout).wait_until(be.visible):
            self.spinner.with_(timeout=90).should(be.hidden)
