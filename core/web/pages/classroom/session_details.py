from datetime import timedelta

from selene import browser, have

from core.web.elements.base_element import BaseElement
from core.web.pages.base_page import DynamicUrlPage
from util.web.assist.allure import report
from util.web.assist.selene.extended import by


class SessionDetailsPage(DynamicUrlPage):
    def __init__(self):
        super().__init__(url_template="classroom/outputs/{session_id}")
        self.head_navigation = OutputMenuHeader()
        self.date_and_time = self.browser.element("//div[contains(@class, 'Description_item')][1]")
        self.duration = self.browser.element("//div[contains(@class, 'Description_item')][2]")
        self.recording_player = self.browser.element(by.class_contains("RecordingsPlayer_videoContainer"))

    @report.step
    def parse_to_timedelta(self, duration_text):
        duration_list = duration_text.split(" ")
        hours = int(duration_list[0].replace("h", ""))
        minute = int(duration_list[1].replace("m", ""))
        seconds = int(duration_list[2].replace("s", ""))
        return timedelta(hours=hours, minutes=minute, seconds=seconds)

    @staticmethod
    def remove_leading_zeros(time_str):
        if time_str.startswith("0"):
            return time_str[1:]
        return time_str


class OutputMenuHeader(BaseElement):
    def __init__(self):
        super().__init__()
        self._container = browser.element(by.class_starts_with("Tabs_header"))
        self.header_items = self._container.all(".//button")

    @report.step
    def click_item(self, name: str):
        self.header_items.element_by(have.exact_text(name)).click()
