from selene import browser

from core.web.elements.dynamic.more_menu import LmsMoreMenu
from core.web.elements.dynamic.table import StandardCellsTable, TableRowWithMenu
from core.web.pages.lms.content_library_pages.library_base import LibraryPageBase
from util.web.assist.allure import report
from util.web.assist.selene.extended import by


class ScormLibraryPage(LibraryPageBase):
    def __init__(self):
        super().__init__()
        self.create_new_button = browser.element("//button[@aria-label='Create New']")
        self.modified_column_header = browser.element("//td[@aria-label='Column Last modified']")
        self.more_menu = LmsMoreMenu(
            browser.element(
                '//table[@class="dx-datagrid-table dx-datagrid-table-fixed"]'
                '//tr[contains(@class, "dx-row dx-data-row dx-row-lines")]'
            )
        )
        self.table: StandardCellsTable[TableRowWithMenu] = StandardCellsTable(
            root=browser.element(by.class_starts_with("DataGridViewer")),
            table_header_locator=".//table[not(contains(@class, 'dx-pointer-events-none'))]//tr[contains(@class, "
            "'dx-header-row')]",
            header_cell_locator=".//td",
            row_locator=".//div[contains(@class, 'dx-datagrid-rows')]//tr[contains(@class, 'dx-row-lines')]",
            column_names=("Title", "Code", "State", "Last modified", "Created by", "Modified by", "Team"),
        )

    @report.step
    def filter_by_code(self, code: str):
        index = self.table._get_column_index_by_name("Code")
        filter_input = browser.element(f"(//input[@aria-label='Filter cell'])[{index - 1}]")
        filter_input.clear()
        filter_input.send_keys(code)
        self.table.should_have_a_row_with(column_name="Code", value=code)
        return self

    @report.step
    def click_edit_for_organization(self, organization_code: str):
        self.filter_by_code(organization_code).more_menu.select_item_by_text("Edit")

    @report.step
    def click_publish_for_organization(self, organization_code: str):
        self.filter_by_code(organization_code).more_menu.select_item_by_text("Publish")
