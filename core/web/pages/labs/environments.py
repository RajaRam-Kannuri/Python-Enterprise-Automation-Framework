from selene import Collection, Element, be, browser

from core.web.elements.dynamic.form_control import TextFormControl
from core.web.elements.dynamic.table import Row, StandardCellsTable, Table, TableRowWithMenu, TableWithFilters
from core.web.elements.lab.form_controls import VMTextFormControl
from core.web.elements.static.modal import Modal
from core.web.elements.static.slide_menu import SlideMenu
from core.web.elements.static.toast import NewToastItem
from core.web.pages.platform_base_page import PlatformBaseDynamicPage, PlatformBaseStaticPage
from util.web.assist.allure import report
from util.web.assist.selene.extended import by


class DeleteEnvModal(Modal):
    def __init__(self):
        super().__init__()
        self.cancel_button = self.footer.element(by.text("Cancel"))
        self.delete_button = self.footer.element(by.text("Delete"))


class EditEnvModal(Modal):
    def __init__(self):
        super().__init__()
        self.name_form_control = TextFormControl(root=self.section, by_placeholder="Environment name")
        self.cancel_button = self.footer.element(by.text("Cancel"))
        self.save_button = self.footer.element(by.text("Save changes"))


class VmRenameModal(Modal):
    def __init__(self):
        super().__init__()
        self.name_form_control = TextFormControl(root=self.section, by_placeholder="Virtual machine name")
        self.cancel_button = self.footer.element(by.text("Cancel"))
        self.save_button = self.footer.element(by.text("Save changes"))


class ConfirmChangesModal(Modal):
    def __init__(self):
        super().__init__()
        self.cancel_button = self.footer.element(by.text("Cancel"))
        self.continue_button = self.footer.element(by.text("Continue"))


class EnvironmentsSlideMenu(SlideMenu):
    def __init__(self):
        super().__init__()
        self.rename_button = self.controls_header.element(by.text("Rename"))
        self.delete_button = self.controls_header.element(by.text("Delete"))

        # content part
        self.owner_field = self.content.element(self._get_field_locator("Owner"))
        self.updated_field = self.content.element(self._get_field_locator("Last updated"))
        self.provider_field = self.content.element(self._get_field_locator("Provider"))

        # vms part
        self.vms_components = self._container.element(by.class_starts_with("EnvironmentItemsTableComponent_wrapper"))
        self.vms_counter_field = self.vms_components.element(
            by.class_starts_with("EnvironmentItemsTableComponent_header")
        )
        self.vms_table: Table = Table(
            root=self.vms_components,
            row_locator=by.class_starts_with("EnvironmentItemsTableItem_wrapper"),
            locators_dict={
                "Name": by.class_starts_with("EnvironmentItemsTableItem_nameCell"),
                "System": by.class_starts_with("EnvironmentItemsTableItem_providerCell"),
            },
        )
        self.add_vm_button = self.vms_components.element(by.text("Add virtual machine"))
        self.vm_modal = VmRenameModal()
        self.confirm_modal = ConfirmChangesModal()

        # used in labs
        self.used_in_labs_counter_field = self.content.element(by.class_starts_with("UsedInLabsListComponent"))
        self.used_in_labs_collection: Collection = self.content.all(
            by.class_starts_with("UsedInLabsListItem_itemWrapper")
        )


class EnvironmentsPage(PlatformBaseStaticPage):
    def __init__(self):
        super().__init__("labs/libraries#environments")
        self.add_environment_button: Element = browser.element('//button/*[@name="PlusBold"]')
        self.modal_delete_window = DeleteEnvModal()
        self.modal_edit_window = EditEnvModal()
        self.toast = NewToastItem()
        self.table: TableWithFilters[StandardCellsTable[TableRowWithMenu]] = TableWithFilters(
            browser,
            tag_names=("Base", "Custom", "Windows", "Linux", "Created by me", "Used in my labs"),
            table=StandardCellsTable(
                root=browser, column_names=("Name", "Used in labs", "Provider", "Owner", "VMs", "Last updated")
            ),
        )
        self.slide_menu = EnvironmentsSlideMenu()

    @report.step
    def make_slide_menu_opened_for(self, image_name):
        if not self.table.results.is_row_presented(column_name="Name", value=image_name):
            self.table.search(image_name)
        self.table.results.get_row_by_cell_value(column_name="Name", value=image_name).body.click()
        self.slide_menu.name_field.should(be.visible)

    @report.step
    def open_slide_menu_by_env_name(self, image_name):
        self.table.get_row_smartly(column_name="Name", value=image_name).body.click()
        self.slide_menu.name_field.should(be.visible)


class EditVMPage(PlatformBaseDynamicPage):
    """Opens, when user edit virtual machines in environments"""

    def __init__(self):
        super().__init__(url_template="")
        self._container = browser.element(by.class_starts_with("EditVirtualMachinePage"))
        self.header = self._container.element("header")
        self.name_form_control = VMTextFormControl(root=self._container, by_label="Name new virtual machine")
        self.amount_form_control = VMTextFormControl(root=self._container, by_label="If you need multiple")
        self.image_selector_table: TableWithFilters[Table[Row]] = TableWithFilters(
            root=browser.element(by.class_starts_with("ListFieldWithFilterBar")),
            tag_names=("Recently used", "Base", "Custom", "Windows", "Linux"),
            filters_locator=by.class_starts_with("ListFieldWithFilterBar_filterBar"),
            table=Table(
                root=browser.element(by.class_starts_with("ListFieldWithFilterBar")),
                row_type=Row,
                locators_dict={
                    "Image name": by.class_starts_with("RadioGroupVirtualList_label"),
                    "System": by.class_starts_with("RadioGroupVirtualList_info"),
                },
                row_locator=by.class_starts_with("Radio-module_wrapper"),
            ),
        )
        self.confirm_button = self._container.element('.//button[@aria-label="submit"]')
        self.search = self._container.element('//*[@placeholder="Search"]')
