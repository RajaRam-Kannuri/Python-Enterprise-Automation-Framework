import typing
from time import sleep

from selene import Element, be, browser, have

from core.web.elements.dynamic.more_menu import BaseMenu, MoreMenu
from core.web.elements.dynamic.table import Row, Table
from core.web.elements.static.modal import Modal, OldModal
from core.web.elements.static.toast import NewToastItem, OldToastItem
from core.web.pages.platform_base_page import PlatformBaseDynamicPage, PlatformBaseStaticPage
from util.web.assist.allure import report
from util.web.assist.selene.extended import by


class LabsMoreMenu(BaseMenu):
    def __init__(
        self,
        root: Element,
        open_menu_button_locator: str = ".btn-menu",
        opened_menu_locator: str = "//*[contains(@class,'menuable__content__active')]",
        item_locator: str = "div.menu-lab-item",
        tooltip_locator: str = '//div[contains(@class, "v-tooltip__content")]/span',
    ):
        super().__init__(root, open_menu_button_locator, opened_menu_locator, item_locator, tooltip_locator)
        self.delete_menu_option = self.menu_items.element_by(have.text("Delete"))
        # hover shows the tooltip only for the text element only
        self.delete_menu_text = self.delete_menu_option.element("span")


class LabsTile(Row):
    def __init__(self, root: Element, cell_locators: typing.OrderedDict):
        super().__init__(root, cell_locators)
        self.more_menu = LabsMoreMenu(root=root)


class LabsTiledTable(Table):
    """
    A grid with labs cards and more menu attached to each lab card.
    It works great as a child class of Table but actually, it should be inherited from the Grid class
     that should be developed when we see more examples like this.
    """

    def __init__(self, root: Element, locators_dict: dict):
        super().__init__(root, locators_dict, row_locator=".mb-10", row_type=LabsTile)

    @report.step
    def get_lab_tile_by_name(self, name) -> LabsTile:
        return self.get_row_by_cell_value(column_name="lab_name", value=name)


class LabsPage(PlatformBaseStaticPage):
    def __init__(self):
        super().__init__("labs")
        self.labs_view = browser.element("div.page-labs")
        self.delete_lab_button = browser.element('//span[text()="Delete"]')
        self.dropdown_menu = browser.element('//*[@class[contains (., "v-menu__content")]]')
        self.labs = browser.all('//a[@class="lab-item"]')
        self.search_icon = browser.element('//i[@class[contains (., "search-icon")]]')
        self.search_input = browser.element('//input[@placeholder="Search"]')
        self.tiled_table: LabsTiledTable[LabsTile] = LabsTiledTable(
            root=browser.element(".mx-1"), locators_dict={"lab_provider": ".lab-provider", "lab_name": ".lab-title"}
        )
        self.toast = OldToastItem()
        self.add_new_lab_button = browser.element('//button[@data-qa="create-lab-button"]')
        self.published_lab_modal = OldModal()

    @report.step
    def open_drafts(self):
        self.labs_view.element(by.text("Drafts")).click()


class PublishedLabModal(Modal):
    def __init__(self):
        super().__init__()
        self.cancel_lab_publishing_button = self._container.element('//button[text()="Cancel"]')
        self.copy_url_button = self._container.element('.//*[text()="Launch URL"]/ancestor::div[2]/button')
        self.copy_consumer_key_button = self._container.element('.//*[text()="Consumer key"]/ancestor::div[2]/button')
        self.copy_shared_secret_button = self._container.element('.//*[text()="Shared secret"]/ancestor::div[2]/button')
        self.publish_confirm_button = self.footer.element('.//button[text()="Publish"]')
        self.got_it_button = self.footer.element('.//button[text()="Got it"]')


class SingleVLPage(PlatformBaseDynamicPage):
    AUTOSAVE_EVERY_2_SECS = 2

    def __init__(self):
        super().__init__(url_template="labs/virtual-labs/{lab_id}")
        self.header_module = browser.element(by.class_starts_with("Headline-module_header"))
        self.breadcrumbs_area = self.header_module.element(
            './/ul[@class[contains(.,"NavComponent-module_breadcrumbs")]]'
        )
        self.content = browser.element('//div[@class[contains(., "LabOverviewTabContent")]]')
        self.content_tab = browser.element('//button/span[text()="Content"]')
        self.more_menu = MoreMenu(root=self.header_module)
        self.preview_lab_button = browser.element('//button[text()="Preview"]')
        self.publish_lab_button = browser.element('//button[text()="Publish"]')
        self.published_lab_modal = PublishedLabModal()
        self.settings_section = browser.element('//section[@class="settings-section"]')
        self.settings_tab = browser.element('//button/span[text()="Settings"]')
        self.toast = OldToastItem()
        self.toast_new = NewToastItem()
        self.unpublish_lab_button = browser.element('//span[text()="Unpublish"]')

    @report.step
    def open_for_lab(self, lab_id) -> typing.Self:
        browser.open(self.url_template.format(lab_id=lab_id))
        self.attach_current_tab()
        return self

    @report.step
    def should_be_opened(self) -> typing.Self:
        self.content.wait_until(be.present)
        return self

    @report.step
    def wait_until_page_will_be_saved(self, seconds: int) -> typing.Self:
        sleep(seconds)
        return self
