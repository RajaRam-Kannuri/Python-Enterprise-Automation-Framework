from selene import Collection, be, browser

from core.web.elements.dynamic.more_menu import MoreMenu
from core.web.elements.dynamic.table import StandardCellsTable, TableRowWithMenu, TableWithFilters
from core.web.elements.static.modal import Modal
from core.web.elements.static.slide_menu import SlideMenu
from core.web.pages.platform_base_page import PlatformBaseStaticPage
from settings import settings
from util.web.assist.allure import report
from util.web.assist.selene.extended import by


class SessionsSlideMenu(SlideMenu):
    def __init__(self):
        super().__init__()
        self.finish_session_button = self.controls_header.element(by.text("Finish session"))
        self.student_field = self.content.element(self._get_field_locator("Student"))
        self.status_field = self.content.element(self._get_field_locator("Status"))
        self.session_id_field = self.content.element(self._get_field_locator("Session ID"))
        self.start_date_field = self.content.element(self._get_field_locator("Started"))
        self.finish_date_field = self.content.element(self._get_field_locator("Finished"))
        self.table = StandardCellsTable(self._container, column_names=("Task name", "Attempts", "Duration", "Status"))

    @report.step
    def close(self):
        self.close_window_button.click()
        self.name_field.should(be.hidden)
        return self


class FinishSessionModal(Modal):
    def __init__(self):
        super().__init__()
        self.continue_button = self.footer.element(by.text("Continue"))
        self.cancel_button = self.footer.element(by.text("Cancel"))


class SessionsPage(PlatformBaseStaticPage):
    URL = "labs/sessions"

    def __init__(self):
        super().__init__(self.URL)
        self.table: TableWithFilters[StandardCellsTable[TableRowWithMenu]] = TableWithFilters(
            root=browser,
            tag_names=("Active sessions", "In review", "Virtual Lab", "Coding Lab"),
            table=StandardCellsTable(
                root=browser.element("table"),
                column_names=("Lab name", "Session ID", "Student", "Status", "Started", "Finished"),
            ),
        )
        self.finish_session_modal = FinishSessionModal()
        self.slide_menu = SessionsSlideMenu()
        self.more_menu = MoreMenu(root=browser.element('//*[@role="table"]'))
        self.tabs_on_panel: Collection = browser.all('.//*[@role="tablist"]//*[@role="tab"]')

    @report.step
    def open_slide_menu_by_session_id(self, session_id: str):
        self.table.cancel_any_active_tag()
        self.table.results.should_be_loaded()
        self.table.get_row_smartly(column_name="Session ID", value=session_id).body.click()
        if not self.slide_menu.name_field.with_(timeout=settings.recheck_timeout).wait_until(be.visible):
            self.table.get_row_smartly(column_name="Session ID", value=session_id).body.click()
