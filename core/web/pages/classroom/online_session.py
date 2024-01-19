from selene import Element, browser

from core.web.elements.dynamic.dropdowns import BaseDropdown
from core.web.elements.dynamic.table import StandardCellsTable, TableRowWithMenu
from core.web.pages.platform_base_page import PlatformBaseStaticPage
from util.web.assist.selene.extended import by


class OnlineSessionPage(PlatformBaseStaticPage):
    URL = "classroom/sessions"

    def __init__(self):
        super().__init__(self.URL)
        self.create_session_dropdown = BaseDropdown(
            root=browser.element(by.class_contains("Button_button")),
            opened_menu_locator='//*[contains(@class, "dropdown-list dropdown-list-root dropdown-list-vertical")]',
            item_locator='li[role="menuitem"]',
        )
        self.session_table: StandardCellsTable[SessionTableRow] = StandardCellsTable(
            root=browser.element('table[role="table"]'),
            column_names=("Session name", "Host", "State", "Duration", "Scheduled", " "),
            row_type=SessionTableRow,
        )
        self.session_search_input = browser.element(by.class_starts_with("SearchInput_input"))


class SessionTableRow(TableRowWithMenu):
    def __init__(self, root: Element, cell_locators: dict):
        super().__init__(root, cell_locators)
        self.start_session_button = root.element(by.text("Start session"))
