from selene import browser

from core.models.scorm.organization import ScormState
from core.web.elements.dynamic.dropdowns import DropdownWithInput
from core.web.elements.dynamic.form_control import LmsFormControl
from core.web.pages.lms.lms_base_page import LmsBasePage
from core.web.pages.platform_base_page import PlatformBaseDynamicPage
from util.random import random_string
from util.web.assist.allure import report
from util.web.assist.selene.extended import by


class CreateObjectivePage(PlatformBaseDynamicPage, LmsBasePage):
    def __init__(self):
        super().__init__(
            url_template="teach/objectives/wizard/new/form?toolUrl={base_url}launch/{resource_launch_id}",
        )
        self.title_form = LmsFormControl(root=browser.element(by.class_contains("form")), by_label="Title")
        self.code_form = LmsFormControl(root=browser.element(by.class_contains("form")), by_label="Unique code or ID")
        self.create_button = browser.element("//button[@type='submit' and text()='Create objective and continue']")
        self.state_dropdown = DropdownWithInput(root=browser.element(by.class_contains("DetailsForm_value")))

    @report.step
    def create_objective(self, organization_code: str) -> str:
        title = random_string(prefix="TestObjName-")
        self.edit_input_field(field="title", value=title)
        self.edit_input_field(field="code", value=organization_code)
        self.change_state(new_state=ScormState.READY)
        self.create_button.click()

        return title
