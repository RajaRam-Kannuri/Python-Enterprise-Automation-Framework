from selene import be, browser, have

from core.web.pages.platform_base_page import PlatformBaseDynamicPage
from util.web.assist.allure import report


class CoursePage(PlatformBaseDynamicPage):
    def __init__(self):
        super().__init__(url_template="learn/courses/{objective_id}/{objective_workflow_aggregate_id}")
        self.start_button = browser.element("//button[@data-qa='start-course-button']")
        self.course_title = browser.element("//h1[contains(@class,'title')]")
        self.course_result_badge = browser.element("//div[contains(@class,'CourseResultBadge')]")
        self.course_result_info = browser.element("//div[contains(@class,'resultsInfo')]")
        self.review_button = browser.element("//button[@data-qa='review-course-button']")

    @report.step
    def should_be_opened(self, title):
        self.course_title.should(be.visible)
        self.course_title.should(have.text(title))

    @report.step
    def start_course(self):
        self.start_button.click()

    @report.step
    def should_have_score(self, expected_score: int):
        self.course_result_badge.should(be.visible)
        self.course_result_badge.should(have.text(f"{expected_score}%"))

    @report.step
    def should_have_status(self, status_text: str):
        self.course_result_info.should(be.visible)
        self.course_result_info.should(have.text(status_text))
