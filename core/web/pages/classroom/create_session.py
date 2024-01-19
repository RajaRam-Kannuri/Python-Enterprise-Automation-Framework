from datetime import timedelta

from selene import browser

from core.web.elements.dynamic.dropdowns import DropdownWithInput
from core.web.elements.dynamic.form_control import ClassroomFormControl, DateFormControl
from core.web.pages.platform_base_page import PlatformBaseStaticPage
from util.web.assist.allure import report
from util.web.assist.selene.extended import by


class TimeDropdownWithInput(DropdownWithInput):
    def __init__(
        self,
        root,
        opened_menu_locator: str = './/*[starts-with(@class, "MenuList-module_menuList")]',
        item_locator: str = './/*[starts-with(@class, "Option-module_mainInfo")]',
    ):
        super().__init__(root, opened_menu_locator, item_locator)


class CreateSessionPage(PlatformBaseStaticPage):
    URL = "classroom/sessions/create"

    def __init__(self):
        super().__init__(self.URL)
        self.class_selection_dropdown = DropdownWithInput(
            root=browser.element(by.class_contains("Select_input")),
            opened_menu_locator='.//*[starts-with(@class, "MenuList_menuList")]',
            item_locator='.//*[starts-with(@class, "Option_mainInfo")]',
        )

        self.session_date_input = DateFormControl(
            root=browser.element(by.class_contains("SessionForm_content")), by_placeholder="Set up the date and time"
        )
        self.start_time_dropdown = TimeDropdownWithInput(
            root=browser.all(by.class_contains("Select-module_wrapper"))[0]
        )
        self.end_time_dropdown = TimeDropdownWithInput(root=browser.all(by.class_contains("Select-module_wrapper"))[-1])
        self.displayed_time_duration = browser.element(by.class_contains("TimesPicker_duration"))

        self.guest_link_toggle_checkbox = browser.element(by.class_contains("Switcher-module_input"))
        self.guest_alert_message = browser.element(by.class_contains("Alert-module_wrapper"))
        self.guest_session_link = browser.element('.//input[contains(@id, "guestLink")]')
        self.upload_files_button = browser.element(by.class_contains("Button-module_primary"))
        self.file_search_input = browser.element(by.class_starts_with("SearchInput_input"))
        self.file_checkbox = browser.element(by.class_starts_with("Checkbox-module_checkbox"))
        self.close_file_list_button = browser.element(by.class_starts_with("IconButton-module_button"))

        self.create_session_button = browser.element(by.text("Create session"))
        self.update_session_button = browser.element(by.text("Update session"))

        self.name_form = ClassroomFormControl(
            root=browser.element(by.class_contains("SessionForm_content")), by_label="Name of your online session"
        )
        self.description_form = ClassroomFormControl(
            root=browser.element(by.class_contains("SessionForm_content")),
            by_label="Add a short description of agenda and links to important materials",
        )

    @report.step
    def set_session_time(self, start, end):
        start_time = start.strftime("%H:%M")
        end_time = end.strftime("%H:%M")

        self.start_time_dropdown.select_item_by_text(start_time)
        self.end_time_dropdown.select_item_by_text(end_time)

    @report.step
    def upload_session_file(self, file_name):
        self.upload_files_button.click()
        self.file_search_input.type(file_name)
        self.file_checkbox.click()
        self.close_file_list_button.click()

    @report.step
    def round_time(self, time_input, round_to=15 * 60):
        return time_input + timedelta(seconds=round_to - (time_input.minute * 60 + time_input.second) % round_to)
