from selene import Element, be, browser

from core.web.elements.base_element import BaseElement
from core.web.elements.dynamic.more_menu import OldMoreMenu
from core.web.elements.dynamic.table import Table
from core.web.pages.labs.lab_pages import SingleVLPage
from settings import settings
from test_data import RESOURCES_PATH
from util.web.assist.allure import report
from util.web.assist.selene.extended import by


class DescriptionSection(BaseElement):
    def __init__(self, root: Element):
        super().__init__()
        self._container = root.element(
            './/*[contains(@class, "settings-section-wrapper") '
            'and .//h3[text()="Cover image, description, labels"]]/ancestor::div[1]'
        )
        self.cover = self._container.element("input[type=file]")
        self.lab_name_input = self._container.element(".//h2")
        self.description_placeholder = self._container.element('.//*[@class="js-tiptap-container"]//p')
        self.empty_cover_image = self._container.element(
            './/*[@class="image-selector image-empty"]|.//*[@class="image-selector image-error"]'
        )
        self.label_section = self._container.element(by.class_starts_with("labels__wrapper"))
        self.label_input = self.label_section.element("input")
        self.delete_label_button = self._container.element(by.class_starts_with("is-clickable is-delete"))
        self.translation_status = self._container.element(by.class_starts_with("TranslationStatus"))
        self.translate_button = self._container.element('.//button[text()="Translate"]')
        self.approve_translation_button = self._container.element('.//button[text()="Approve"]')

    @report.step
    def upload_cover(self, path):
        self.cover.send_keys(str(RESOURCES_PATH / path))


class EnvironmentSection(BaseElement):
    def __init__(self, root: Element):
        super().__init__()
        self._container = root.element(
            './/*[contains(@class, "EnvironmentSettingsSection") and' ' .//h3[text()="Environment"]]/..'
        )
        self.loading_vm_icon = self._container.element('.//*[@class="progress-icon-wrapper"]')
        self.workspace_name = self._container.element(
            by.class_starts_with("EnvironmentSettingsSectionComponent_workspaceName")
        )
        self.table = Table(
            root=self._container,
            locators_dict={
                "Name": './/*[@class[contains(., "nameCell")]]',
                "System type": './/*[@class[contains(., "providerCell")]]',
            },
            row_locator='.//*[@class[contains(., "EnvironmentSettingsSectionComponent_tableWrapper")]]//tbody//tr',
        )
        self.add_env_button = self._container.element(by.text("Add virtual machine"))
        self.more_menu = OldMoreMenu(root=self._container)
        self.running_vm_icon = self._container.element('.//*[@class="running-icon"]')


class SettingsVLPage(SingleVLPage):
    def __init__(self):
        super().__init__()
        self.section_description = DescriptionSection(root=self.settings_section)
        self.section_environment = EnvironmentSection(root=self.settings_section)
        self.spinner = browser.element('//*[@data-testid="spinner"]')

    @report.step
    def wait_until_spinners_are_gone(self):
        if self.spinner.with_(timeout=settings.recheck_timeout).wait_until(be.visible):
            self.spinner.should(be.hidden)
