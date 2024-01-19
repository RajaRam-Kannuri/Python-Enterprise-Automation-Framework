from selene import browser, have

from core.web.elements.base_element import BaseElement
from core.web.elements.dynamic.dropdowns import ProfileDropdown
from core.web.pages.base_page import DynamicUrlPage, StaticUrlPage
from util.web.assist.allure import report
from util.web.assist.selene.extended import by


class SideMenu(BaseElement):
    MENU_LOCATOR = ".//li//a"

    def __init__(self):
        super().__init__()
        self._container = browser.element(by.class_starts_with("SidebarPanelComponent-module_nav"))
        self.menu_elements = self._container.all(f"{self.MENU_LOCATOR}")
        self.tooltip = self.menu_elements.all(by.class_starts_with("HamburgerItemComponent-module_label"))

    def _get_menu_item_for_title(self, menu_name):
        described_element = self.menu_elements.element_by(have.attribute("aria-label").value_containing(menu_name)).as_(
            f'with title "{menu_name}"'
        )
        described_element.previous_name_chain_element = self.menu_elements
        return described_element

    def _get_submenu_item_for_title(self, submenu_name):
        described_element = self.tooltip.element_by(have.text(submenu_name)).hover().as_(f'with title "{submenu_name}"')
        described_element.previous_name_chain_element = self.tooltip
        return described_element

    @report.step
    def open_menu_by_name(self, menu_name, submenu_name=None):
        if submenu_name:
            self._get_menu_item_for_title(menu_name).hover()
            self._get_submenu_item_for_title(submenu_name).click()
        else:
            self._get_menu_item_for_title(menu_name).click()


class Profile(BaseElement):
    def __init__(self):
        super().__init__()
        self.profile_icon = browser.element(by.class_contains("HeaderUserDefaultAvatar"))
        self.language_dropdown = ProfileDropdown(root=browser.element(by.class_name("dropdown-list-submenu-title")))


class MainHeader(BaseElement):
    def __init__(self):
        super().__init__()
        self.container = browser.element(by.class_starts_with("Headline-module_header"))
        self.header_items = self.container.all(".//li//a")
        self.profile = Profile()

    @report.step
    def click_item(self, name: str):
        self.header_items.element_by(have.exact_text(name)).click()


class PlatformBaseStaticPage(StaticUrlPage):
    """
    This is a base page for static (with a static url) platform pages (after a user logged in).
    """

    def __init__(self, url):
        super().__init__(url)
        self.page_title = browser.element("h1")
        self.control_sidebar = SideMenu()
        self.main_header = MainHeader()


class PlatformBaseDynamicPage(DynamicUrlPage):
    """
    This is a base page for static (with a dynamic url) platform pages (after a user logged in).
    """

    def __init__(self, url_template):
        super().__init__(url_template=url_template)
        self.page_title = browser.element("h1")
        self.control_sidebar = SideMenu()
        self.main_header = MainHeader()
