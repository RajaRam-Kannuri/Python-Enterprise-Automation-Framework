from selene import browser

from core.web.elements.dynamic.form_control import ClassroomFormControl
from core.web.elements.dynamic.table import StandardCellsTable, TableRowWithMenu
from core.web.pages.platform_base_page import PlatformBaseDynamicPage
from util.web.assist.selene.extended import by


class ClassroomSetupPage(PlatformBaseDynamicPage):
    def __init__(self):
        super().__init__(url_template="classroom/sessions/{classroom_id}")
        self.description_input_field = browser.element(by.class_starts_with("Textarea-module_textarea"))
        self.save_button = browser.element(by.text("Save and exit"))
        self.check_input_visibility = browser.element('//input[contains(@class,"Input-module_input") and @value != ""]')
        self.check_image_visibility = browser.element('//img[contains(@class, "CoverImageUploader")]')
        self.file_input = browser.element('input[type="file"]')
        self.table: StandardCellsTable[TableRowWithMenu] = StandardCellsTable(
            root=browser.element('table[role="table"]'), column_names=("Name", "Type", "Used in this class")
        )
        self.name_form = ClassroomFormControl(
            root=browser.element(by.class_contains("ClassroomForm_formContainer")),
            by_placeholder="Name of the class, lecture, or lesson",
        )
