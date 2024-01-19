import re

from selene import Collection, Element, be, browser, have

from core.web.elements.dynamic.dropdowns import DropdownWithInput
from core.web.elements.dynamic.form_control import TextFormControl
from core.web.elements.dynamic.table import StandardCellsTable, TableRowWithMenu, TableWithFilters
from core.web.elements.lab.loading_view import LoadingView
from core.web.elements.static.modal import Modal
from core.web.elements.static.slide_menu import SlideMenu
from core.web.elements.static.toast import NewToastItem
from core.web.pages.platform_base_page import PlatformBaseDynamicPage, PlatformBaseStaticPage
from settings import settings
from util.web.assist.allure import report
from util.web.assist.selene.extended import by


class ImagesModal(Modal):
    def __init__(self):
        super().__init__()
        self.name_form_control = TextFormControl(root=self.section, by_placeholder="Image name")
        self.provider_dropdown = DropdownWithInput(
            self.section.element('.//label[text()="Choose provider"]/parent::div')
        )
        self.base_image_dropdown = DropdownWithInput(
            self.section.element('.//div[contains(@class, "CreateImageForm_baseImageSelector")]')
        )
        self.create_button = self.footer.element(by.text("Create"))
        self.cancel_button = self.footer.element(by.text("Cancel"))


class RenameImageModal(Modal):
    def __init__(self):
        super().__init__()
        self.name_form_control = TextFormControl(root=self.section, by_placeholder="Image name")
        self.rename_button = self.footer.element(by.text("Save changes"))
        self.cancel_button = self.footer.element(by.text("Cancel"))

    @report.step
    def rename_image_to(self, new_name):
        self.name_form_control.fill_with_text(new_name)
        self.rename_button.should(be.enabled).click()
        self._container.should(be.absent)


class ConfirmImageChangeModal(Modal):
    def __init__(self):
        super().__init__()
        self.confirm_button = self.footer.element(by.text("Confirm"))
        self.cancel_button = self.footer.element(by.text("Cancel"))


class ImagesSlideMenu(SlideMenu):
    def __init__(self):
        super().__init__()
        self.change_button = self.controls_header.element(by.text("Change"))
        self.rename_button = self.controls_header.element(by.text("Rename"))
        self.delete_button = self.controls_header.element(by.text("Delete"))

        # content part
        self.id_field = self.content.element(self._get_field_locator("ID"))
        self.os_field = self.content.element(self._get_field_locator("OS"))
        self.provider_field = self.content.element(self._get_field_locator("Provider"))
        self.version_field = self.content.element(self._get_field_locator("Version"))

        # used in labs
        self.used_in_labs_counter_field = self.content.element(by.class_starts_with("UsedInLabsListComponent"))
        self.used_in_labs_collection: Collection = self.content.all(
            by.class_starts_with("UsedInLabsListItem_itemWrapper")
        )


class ImagesPage(PlatformBaseStaticPage):
    URL = "labs/libraries#images"

    def __init__(self):
        super().__init__(self.URL)
        self.create_custom_image_button: Element = browser.element('//button/*[@name="PlusBold"]')
        self.create_custom_image_modal = ImagesModal()
        self.rename_modal = RenameImageModal()
        self.toast = NewToastItem()
        self.table: TableWithFilters[StandardCellsTable[TableRowWithMenu]] = TableWithFilters(
            root=browser.element(by.class_starts_with("TableWithFilter_wrapper")),
            tag_names=("Base", "Custom", "Windows", "Linux"),
            table=StandardCellsTable(
                root=browser.element(by.class_starts_with("Table-module_table")),
                column_names=("Name", "Used in labs", "Provider", "OS", "Version", "ID"),
            ),
        )
        self.slide_menu = ImagesSlideMenu()
        self.confirm_image_change_modal = ConfirmImageChangeModal()

    @report.step
    def open_slide_menu_by_image_name(self, image_name):
        if not self.table.results.is_row_presented(column_name="Name", value=image_name):
            self.table.search(image_name)
        self.table.results.get_row_by_cell_value(column_name="Name", value=image_name).body.click()
        self.slide_menu.name_field.should(be.visible)


class SingleImagePage(PlatformBaseDynamicPage):
    def __init__(self):
        super().__init__(url_template="images/{vm_id}")
        self.content = browser.element("div.viewer-content-holder")
        self.header = browser.element(".viewer-nav")
        self.loading_view = LoadingView(self.content)
        self.save_button = self.header.element(by.text("Save and close"))

    @property
    def opened_vm_id(self):
        browser.should(have.url_containing("/images/"))
        current_url = browser.driver.current_url
        try:
            return re.match(r".*/images/(vm-[\d\w]{,10})$", current_url).group(1)
        except AttributeError:
            raise AttributeError(f'current page is not contain vm_id. presented url = "{current_url}"')

    @report.step
    def wait_vm_loading(self):
        self.loading_view.waiting_text_field.with_(timeout=settings.code_server_starting_timeout).wait_until(be.absent)
        return self

    @report.step
    def save_and_quit(self):
        self.save_button.should(be.present)
        self.loading_view.waiting_text_field.wait_until(have.text("Loading virtual environment"))
        self.loading_view.waiting_text_field.with_(timeout=settings.image_preparation_timeout).wait_until(be.absent)
        self.save_button.click()
