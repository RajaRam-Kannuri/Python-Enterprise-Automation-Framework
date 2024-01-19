from selene import Element, browser

from core.web.elements.base_element import BaseElement
from util.web.assist.allure import report


class BaseToastItem(BaseElement):
    container_locator = None
    text_locator = None

    def __init__(self, root_item=browser):
        super().__init__()
        self._container: Element = root_item.element(self.container_locator)
        self.close_button: Element = self._container.element("button")
        self.text: Element = self._container.element(self.text_locator)

    @report.step
    def close(self):
        self.close_button.click()


class NewToastItem(BaseToastItem):
    container_locator = '//*[contains(@class, "ToastItem-module_notification")]'
    text_locator = './/*[contains(@class, "ToastItem-module_notificationTitle")]'
    message_locator = './/*[contains(@class, "ToastItem-module_notificationMessage")]'

    def __init__(self):
        super().__init__()
        self.message: Element = self._container.element(self.message_locator)


class OldToastItem(BaseToastItem):
    container_locator = '//*[@id="toast-hub"]'
    text_locator = './/*[contains(@class, "toast-content")]'
