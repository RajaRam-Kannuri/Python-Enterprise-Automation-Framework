import time

from selene import be, browser, have

from core.models.lms.lms_base import to_camel_case
from core.models.scorm.organization import DisplayMode
from core.web.elements.dynamic.frame import Frame
from core.web.pages.platform_base_page import PlatformBaseDynamicPage
from settings import settings
from util.web.assist.allure import report
from util.web.assist.selene.extended import by


class CourseContentPage(Frame, PlatformBaseDynamicPage):
    def __init__(self):
        super().__init__(
            iframe=browser.element("iframe[title='LTI tool iframe']"),
            url_template="learn/courses/{objective_id}/view/content",
        )
        self.section_list = browser.all("//ul[@role='group']/li")
        self.scorm_player_iframe = MenuFrame()
        self.spinner = browser.element('//*[@data-testid="spinner"]')
        self.submit_button = browser.element("a#submit-btn")
        self.close_button = browser.element("//a[@id='close-btn']")
        self.submit_confirm_button = browser.element("button#submit-confirm-btn")

    @report.step
    def check_screen(self, display_mode: DisplayMode):
        lti_card = browser.element(by.class_contains(f"LtiCardIframe-module_{to_camel_case(display_mode.name)}"))
        lti_card.should(be.visible)

    @report.step
    def wait_for_spinner_to_hide(self):
        if self.spinner.with_(timeout=settings.recheck_timeout).wait_until(be.visible):
            self.spinner.should(be.hidden)

    @report.step
    def pass_course(self):
        # The spinner inside the first iframe delays the automation code
        # from accessing the content in the second iframe
        # It is a scorm package specific issue, sleep solves the issue
        time.sleep(1)
        with self.make_active() as lti_frame:
            with lti_frame.scorm_player_iframe.make_active() as menu_frame:
                menu_frame.section_list.should(have.size_greater_than(0))
                for section in menu_frame.section_list:
                    section.click()
            lti_frame.submit_button.hover()
            lti_frame.submit_button.should(be.visible).click()
            lti_frame.submit_confirm_button.click()

    @report.step
    def review_course(self):
        # The spinner inside the first iframe delays the automation code
        # from accessing the content in the second iframe
        # It is a scorm package specific issue, sleep solves the issue
        time.sleep(1)
        with self.make_active() as lti_frame:
            with lti_frame.scorm_player_iframe.make_active() as menu_frame:
                if menu_frame.resume.wait_until(be.visible):
                    menu_frame.resume.click()
                menu_frame.section_list.should(have.size_greater_than(0))
                for section in menu_frame.section_list:
                    section.click()
            lti_frame.close_button.hover()
            lti_frame.close_button.should(be.visible)
            lti_frame.submit_button.should(be.not_.present)


class MenuFrame(Frame):
    def __init__(self):
        super().__init__(iframe=browser.element("//iframe[contains(@src,'resource-launches')]"))
        self.section_list = browser.all("//ul[@role='group']/li")
        self.resume = browser.element("[aria-label='Resume']")
