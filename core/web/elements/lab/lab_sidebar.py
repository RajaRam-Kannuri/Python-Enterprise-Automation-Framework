from selene.support.conditions import be, have
from selene.support.shared import browser

from core.web.elements.base_element import BaseElement
from settings import settings
from util.web.assist.allure import report
from util.web.assist.selene.extended import by


class LabSidebar(BaseElement):
    ROOT_LOCATOR = None

    def __init__(self, root=browser):
        super().__init__()
        self._container = root.element(self.ROOT_LOCATOR)
        self.content = self._container.element(".sidebar-content")
        self.task_details = self.content.element(".task-detail-wrapper")
        self.tasks_boxes = self.task_details.all("section.instruction")
        self.footer = self._container.element(".sidebar-footer")
        self.next_button = self.footer.element('.//*[text()="Next"]/ancestor::button')
        self.close_lab_button = self.footer.element('.//span[text()="Close"]')
        self.back_button = self.footer.element(by.text("Back"))
        self.finish_button = self.footer.element(by.text("Finish"))

    @report.step
    def go_next(self):
        self.next_button.click()

    @report.step
    def go_back(self):
        self.back_button.click()

    @report.step
    def finish(self):
        self.finish_button.click()

    @report.step
    def close_lab(self):
        tabs_amount_before = len(browser.driver.window_handles)
        self.close_lab_button.should(be.enabled).click()
        browser.with_(timeout=settings.coding_lab_general_timeout).should(have.tabs_number(tabs_amount_before - 1))
        browser.switch_to_tab(0)

    @report.step
    def task_with_index_should_be_succeed(self, task_index):
        task_succeed_class = "completed"
        self.tasks_boxes[task_index].should(have.css_class(task_succeed_class))

    @report.step
    def task_with_index_should_be_failed(self, task_index):
        task_failed_class = "failed"
        self.tasks_boxes[task_index].should(have.css_class(task_failed_class))
