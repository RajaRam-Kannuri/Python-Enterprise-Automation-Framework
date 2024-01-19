from selene.core import query
from selene.core.entity import Element
from selene.support.conditions import be, have
from selene.support.shared import browser

from core.web.elements.base_element import BaseElement
from settings import settings
from util.web.assist.allure import report


class LoadingView(BaseElement):
    def __init__(self, root: Element):
        super().__init__()
        self._container: Element = root.element('.//div[contains(@class, "LoadingView_wrapper")]')
        self.waiting_text_field: Element = self._container.element("h2")

    def is_visible(self):
        return self.waiting_text_field.matching(be.present)

    @property
    def waiting_text(self) -> str:
        return self.waiting_text_field.get(query.text)


class LoadingLabView(BaseElement):
    wait_texts_dict = {
        "English": "Wait a moment...",
        "Deutsch": "Warten Sie einen Augenblick",
        "Français": "Veuillez patienter…",
    }
    TIMEOUT = 180

    def __init__(self, root=None):
        super().__init__()
        self._container = root or browser.element(".loading-wrapper")
        self.waiting_message = self._container.element(".placeholder-title")

    @report.step
    def wait_until_loads(self, language="English"):
        if self.waiting_message.with_(timeout=settings.recheck_timeout).wait_until(
            have.text(self.wait_texts_dict[language])
        ):
            self.waiting_message.with_(timeout=self.TIMEOUT).should(be.hidden)
