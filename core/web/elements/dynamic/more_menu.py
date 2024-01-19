from selene.core.entity import Element
from selene.support.conditions import have

from core.web.elements.dynamic.dropdowns import AbstractMenuElement
from core.web.elements.lms.settings_control import SettingsControl
from util.web.assist.allure import report
from util.web.assist.selene.extended import by


class BaseMenu(AbstractMenuElement):
    def __init__(
        self,
        root: Element,
        open_menu_button_locator: str,
        opened_menu_locator: str,
        item_locator: str,
        tooltip_locator: str = None,
    ):
        super().__init__(root, opened_menu_locator=opened_menu_locator, item_locator=item_locator)
        self.open_menu_button: Element = root.element(open_menu_button_locator)
        if tooltip_locator:
            self.tooltip: Element = self.opened_menu.element(tooltip_locator)

    @property
    def trigger(self) -> Element:
        return self.open_menu_button


class MoreMenu(BaseMenu):
    def __init__(
        self,
        root: Element,
        open_menu_button_locator: str = by.class_starts_with("MoreButton-module_button"),
        opened_menu_locator: str = '//*[contains(@class,"MoreButton-module_overlay")]',
        item_locator: str = "li.dropdown-list-item",
        tooltip_locator: str = '[role="tooltip"]',
    ):
        super().__init__(root, open_menu_button_locator, opened_menu_locator, item_locator, tooltip_locator)


class OldMoreMenu(MoreMenu):
    def __init__(
        self,
        root,
        open_menu_button_locator: str = './/*[@class="more-icon"]/ancestor::button',
        opened_menu_locator: str = 'div[role="menu"]',
        item_locator: str = by.class_name("v-list-item"),
    ):
        super().__init__(root, open_menu_button_locator, opened_menu_locator, item_locator)


class MoreMenuThirdOption(BaseMenu):
    def __init__(
        self,
        root: Element,
        open_menu_button_locator: str = by.class_starts_with("IconButton-module_button"),
        opened_menu_locator: str = "div.szh-menu-container ul[role=menu]",
        item_locator="li",
    ):
        super().__init__(root, open_menu_button_locator, opened_menu_locator, item_locator)


class MoreMenuWithSubMenu(BaseMenu):
    def __init__(
        self,
        root: Element,
        open_menu_button_locator: str = by.class_contains("Item_more"),
        opened_menu_locator: str = "div.szh-menu-container ul[role=menu]",
        item_locator: str = "li",
    ):
        super().__init__(root, open_menu_button_locator, opened_menu_locator, item_locator)

    @report.step
    def select_menu_and_submenu_by_text(self, menu, submenu):
        self.make_opened()
        submenu_element = (
            MoreMenuThirdOption(
                root=self.menu_items.element_by(have.text(menu)), open_menu_button_locator=by.xpath(".")
            )
            .as_(f"submenu of {menu}")
            .set_previous_name_chain_element(self)
        )
        submenu_element.select_item_by_text(submenu)


class LmsMoreMenu(MoreMenu):
    def __init__(
        self,
        root,
        open_menu_button_locator: str = by.class_contains("ActionsMenu_menuBtn"),
        opened_menu_locator: str = '//div[@class="dx-overlay-wrapper"]//div[@class="dx-submenu"]',
        item_locator: str = ".//li[@class='dx-menu-item-wrapper']",
    ):
        super().__init__(root, open_menu_button_locator, opened_menu_locator, item_locator)


# TODO: It will be refactored using LMSCheckboxForm when it's implemented.
class LibrarySettingsMoreMenu(MoreMenu):
    def __init__(
        self,
        root,
        open_menu_button_locator: str = by.class_starts_with("UiCollapsible-module_header"),
        opened_menu_locator: str = "//div[div[contains(@class,'ScormSettings_line')]]",
        item_locator: str = "//div[contains(@class,'ScormSettings_line')]",
    ):
        super().__init__(root, open_menu_button_locator, opened_menu_locator, item_locator)

    def get_setting_control(self, setting_name):
        return SettingsControl(self._container, setting_name)
