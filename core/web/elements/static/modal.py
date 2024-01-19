from selene.core.entity import Element
from selene.support.conditions import be
from selene.support.shared import browser

from core.web.elements.base_element import BaseElement
from util.web.assist.allure import report


class Modal(BaseElement):
    container_locator = ".ReactModal__Content"
    section_locator = "section"
    header_locator = "header h2"

    def __init__(self, browser_instance=browser):
        super().__init__()
        self._container: Element = browser_instance.element(self.container_locator)
        self.close_button: Element = self._container.element("header button")
        self.header: Element = self._container.element(self.header_locator)
        self.section: Element = self._container.element(self.section_locator)
        self.footer = self._container.element("footer")

    @report.step
    def close(self):
        self.close_button.click()

    def make_closed(self):
        if self._container.matching(be.visible):
            self.close()


class OldModal(Modal):
    container_locator = ".modal-container"


class FloatingModal(Modal):
    container_locator = 'div[data-testid="file-upload-drag-modal"]'
