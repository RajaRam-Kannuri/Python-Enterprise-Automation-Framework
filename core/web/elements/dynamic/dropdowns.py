import abc

from selene import Collection, Element, be, have

from core.web.elements.base_element import BaseElement
from util.web.assist.allure import report


class AbstractMenuElement(BaseElement, abc.ABC):
    def __init__(self, root: Element, opened_menu_locator: str, item_locator: str):
        super().__init__()
        self._container = root
        self.opened_menu: Element = self._container.element(opened_menu_locator)
        self.menu_items: Collection = self.opened_menu.all(item_locator)

    @property
    @abc.abstractmethod
    def trigger(self) -> Element:
        """
        menu opening element
        """
        ...

    @report.step
    def open_menu(self):
        self.trigger.click()
        self.menu_items.by(be.visible).should(have.size_greater_than(0))

    def is_menu_opened(self) -> bool:
        result = self.opened_menu.matching(be.visible)
        return result

    @report.step
    def close_already_opened_menu(self):
        self.trigger.press_enter()

    @report.step
    def make_opened(self):
        if self.is_menu_opened():
            self.close_already_opened_menu()
        self.open_menu()

    @report.step
    def select_item_by_text(self, text):
        self.make_opened()
        self.menu_items.element_by(have.text(text)).click()

    @report.step
    def select_item_by_index(self, index):
        self.make_opened()
        self.menu_items[index].click()


class BaseDropdown(AbstractMenuElement):
    def __init__(self, root: Element, opened_menu_locator: str, item_locator: str, selected_text_locator: str = None):
        super().__init__(root, opened_menu_locator, item_locator)
        if selected_text_locator:
            self.selected_text = self._container.element(selected_text_locator)

    @property
    def trigger(self):
        return self._container


class Dropdown(BaseDropdown):
    def __init__(
        self,
        root,
        opened_menu_locator: str = 'div[role="listbox"]',
        item_locator: str = ".v-list-item",
        selected_text_locator: str = "div.selection-overflow",
    ):
        super().__init__(root, opened_menu_locator, item_locator, selected_text_locator)


class DropdownWithInput(BaseDropdown):
    def __init__(
        self,
        root,
        opened_menu_locator: str = './/div[contains(@class, "Menu-module")]',
        item_locator: str = './/div[contains(@class, "Option-module_option_")]',
        selected_text_locator: str = None,
    ):
        super().__init__(root, opened_menu_locator, item_locator, selected_text_locator)
        self.input = self._container.element("input")

    @report.step
    def fill_search_form(self, text):
        self.input.type(text)

    @report.step
    def select_item_by_text(self, text):
        self.make_opened()
        self.input.clear().type(text)
        self.menu_items.element_by(have.text(text)).click()


class ProfileDropdown(BaseDropdown):
    def __init__(
        self,
        root,
        opened_menu_locator: str = '//*[@class="dropdown-list dropdown-list-sub dropdown-list-vertical"]',
        item_locator: str = 'li[role="menuitem"]',
    ):
        super().__init__(root, opened_menu_locator, item_locator)

    @report.step
    def open_menu(self):
        self._container.should(have.text("Language"))
        self._container.hover()
        self.menu_items.first.should(be.visible)
