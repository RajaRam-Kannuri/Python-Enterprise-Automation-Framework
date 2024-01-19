from selene import Collection, be, browser

from core.web.elements.lab.lab_sidebar import LabSidebar
from core.web.elements.lab.loading_view import LoadingLabView
from core.web.elements.static.toast import OldToastItem
from core.web.pages.labs.preview_lab_pages.base_preview import BasePreviewPage
from util.web.assist.allure import report
from util.web.assist.selene.extended import by


class PreviewLabPage(BasePreviewPage):
    def __init__(self):
        super().__init__(url_template="labs/viewer/{lab_id}?session_id={session_id}")
        self._container = browser.element(by.class_name("site-content"))
        self.breadcrumb_area = browser.element('//*[@class="ui-navbar-item breadcrumb"]/span')
        self.close_lab_button = self._container.element('.//span[text()="Close"]')
        self.help_icon = self._container.element("i.i-question-circle")
        self.fullscreen_button = self._container.element('.//button[@class="tab-header__fullscreen"]')
        self.start_lab_button = self._container.element('.//*[@class="lab-content"]//button')
        self.lab_preload = LoadingLabView(root=self._container.element(".placeholder-empty"))
        self.lab_sidebar = VmLabSidebar()
        self.lab_minimized_sidebar = VmMinimizedSidebar()
        self.toast = OldToastItem()
        self.vms_tabs: Collection = self._container.all('[role="tab"]')

    @report.step
    def start_a_lab(self):
        self.start_lab_button.should(be.enabled)
        self.start_lab_button.click()


class VmLabSidebar(LabSidebar):
    ROOT_LOCATOR = ".lab-sidebar"

    def __init__(self):
        super().__init__()
        self.content = self._container.element(by.class_starts_with("sidebar-content"))
        self.instructions = self._container.element(".viewer-outline")
        self.lab_name_input = self._container.element(by.class_starts_with("lab-name"))
        self.description_placeholder = self._container.element('.//*[@class="js-tiptap-container"]')
        self.settings_icon = self._container.element("i.i-maintenance")
        self.pause_session_button = self._container.element('.//span[text()="Pause session"]/ancestor::button')
        self.reset_session_button = self._container.element('.//span[text()="Reset session"]/ancestor::button')
        self.restart_icon = self._container.element("i.i-restart")
        self.resume_session_button = self._container.element('.//span[text()="Resume session"]')
        self.lab_session_id = self._container.element('.//div[text()[contains (., "ID")]]')
        self.link = self._container.element(".//li/a")
        self.contact_name = self._container.element(by.class_starts_with("contact-name"))
        self.contact_phone = self._container.element(by.class_starts_with("contact-phone"))
        self.contact_email = self._container.element('//*[@class[contains(., "contact-detail")]]/a')
        self.finish_button = self._container.element('.//span[text()="Finish"]/ancestor::button')
        self.close_lab_button = self._container.element('.//span[text()="Close"]/ancestor::button')


class VmMinimizedSidebar(VmLabSidebar):
    ROOT_LOCATOR = ".navigation-panel__menu"

    def __init__(self):
        super().__init__()
        self.fold_button = self._container.element(by.class_starts_with("navigation-panel__button"))
