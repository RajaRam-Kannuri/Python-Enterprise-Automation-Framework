from selene import be

from core.models.scorm.organization import ScormState
from core.web.pages.base_page import BasePage
from util.web.assist.allure import report


class LmsBasePage(BasePage):
    @report.step
    def edit_input_field(self, field: str, value: str = "", clear_input: bool = False):
        form = getattr(self, f"{field}_form")
        form.input.should(be.not_.blank)
        if clear_input:
            form.input.clear()
        else:
            form.fill_with_text(value)

    @report.step
    def change_state(self, new_state: ScormState):
        self.state_dropdown.select_item_by_text(new_state.name.title())
