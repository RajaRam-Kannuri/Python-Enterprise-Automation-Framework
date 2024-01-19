from selene import Browser, be, browser, have

from core.web.elements.dynamic.dropdowns import Dropdown
from core.web.elements.dynamic.more_menu import MoreMenuThirdOption
from core.web.elements.static.modal import FloatingModal, Modal
from core.web.elements.static.toast import NewToastItem
from core.web.pages.base_page import DynamicUrlPage
from core.web.pages.classroom.session_roles import ModeratorRole, Participant, ParticipantRole, PresenterRole
from util.web.assist.allure import report
from util.web.assist.selene.extended import by


class InstantSessionPage(DynamicUrlPage):
    def __init__(self, browser_instance: Browser = browser):
        super().__init__(url_template="classroom/{session_id}/nopass", browser_instance=browser_instance)
        self.start_session_button = self.browser.element(
            './/div[contains(@class, "ConferenceDetails")]//button[contains(@class,"Button-module_primary")]'
        )
        self.exit_option_button = self.browser.element(by.class_starts_with("VcsToolbar_exit"))
        self.confirmation_text = self.browser.element(by.class_contains("ConferenceDetails_independent"))

        # Toolbar buttons
        self.mic_active_button = self.browser.element(by.class_contains("ToolbarButton_active"))
        self.background_image_button = self.browser.element(by.class_contains("UserVideoPreview_virtualBg"))
        self.blur_background_image = self.browser.element(
            './/*[contains(@class, "VirtualBackgroundsList")]//*[text()="Blur my background"]'
        )
        self.parent_element = self.browser.element(by.class_contains("UserVideoPreview_avatarFooter"))
        self.elements_enabled = self.parent_element.all(by.class_contains("Enabled"))
        self.mic_button = self.browser.element(by.class_contains("UserVideoPreview_mic"))
        self.video_button = self.browser.element(by.class_contains("UserVideoPreview_cam"))
        self.parent_element = self.browser.element(by.class_contains("UserVideoPreview_avatarFooter"))
        self.elements_enabled = self.parent_element.all(by.class_contains("Enabled"))

        # Participant controls
        self.participant_video = self.browser.element(by.class_contains("ParticipantVideo_container"))
        self.participant_name_input = self.browser.element(by.class_contains("Input-module_input"))
        self.participant_list_button = self.browser.element('.//*[contains(@aria-label, "Participants list")]')
        self.participant_list_items = self.browser.all(
            '//*[starts-with(@class, "UsersOfRole_wrap")]//*[starts-with(@class, "Item_item")]'
        )
        self.participant_alignment_indicator = self.browser.element(by.class_contains("FocusLayout_wrap"))
        self.participant_container = Participant(
            root=self.browser.element(
                './/*[text()="Guest participant"]/ancestor::*[contains(@class,"ParticipantVideo_container")]'
            )
        )

        # Side menus and panels
        self.side_menu_element = self.browser.element(
            './/*[contains(@class, "Sidebar_sidebar") and not(contains(@class,"Sidebar_keepaliveHidden"))]'
        )
        self.side_menu_close_button = self.side_menu_element.element(by.class_contains("Sidebar_closeBtn"))

        # Background settings
        self.blur_background_image = self.browser.element(
            './/*[contains(@class, "VirtualBackgroundsList")]//*[text()="Blur my background"]'
        )
        self.background_items = self.browser.all(by.class_contains("Item_text"))
        self.upload_background_image = self.browser.element(
            './/*[contains(@class, "VirtualBackgroundsList_wrap")]//input[@type="file"]'
        )
        self.background_images = self.browser.all(by.class_contains("Item_imageWrap"))
        self.delete_custom_background = self.browser.element('.//button[@aria-label="Delete"]')

        # Roles and others
        self.presenter = PresenterRole(root=self.side_menu_element)
        self.participant = ParticipantRole(root=self.side_menu_element)
        self.moderator = ModeratorRole(root=self.side_menu_element)
        self.toast = NewToastItem()
        self.settings_menu = SettingsMenu()
        self.presenter_list = self.browser.element(
            './/*[contains(@class ,"Accordion-module_title") and contains(text(),"Presenters")]/ancestor::*[4]'
        ).all(by.class_starts_with("Item_name"))
        self.content_dropdown = Dropdown(
            root=self.browser.element('.//*[@aria-label="Share content menu"]'),
            item_locator='li[role="menuitem"]',
            opened_menu_locator='//*[contains(@class, "dropdown-list dropdown-list-root dropdown-list-vertical")]',
        )
        self.pin_participant_button = self.browser.element(by.class_contains("ParticipantVideo_putOnStageBtn"))
        self.participant_pin_icon = self.browser.element('.//button//*[contains(@name,"Pin")]')
        self.participant_alignment_indicator = self.browser.element(by.class_contains("FocusLayout_wrap"))
        self.side_menu_element = self.browser.element(
            './/*[contains(@class, "Sidebar_sidebar") and not(contains(@class,"Sidebar_keepaliveHidden"))]'
        )
        self.side_menu_close_button = self.side_menu_element.element(by.class_contains("Sidebar_closeBtn"))
        self.start_record_button = self.browser.element('.//*[contains(@aria-label, "Start recording")]')
        self.stop_record_button = self.browser.element('.//*[contains(@aria-label, "Stop recording")]')
        self.Session_title = self.browser.element(by.class_contains("ConferenceInfo_title"))
        self.more_button = self.browser.element('.//button[text()="more"]')

        # modals
        self.end_session_modal = EndSessionModal(browser_instance=browser_instance)
        self.doc_picker_modal = DocPickerModal(browser_instance=browser_instance)
        self.more_options_modal = MoreOptionsMenuModal(browser_instance=browser_instance)
        self.recording_modal = SessionRecordingModal(browser_instance=browser_instance)

        # File preview and close button
        self.file_preview = self.browser.element("//div[contains(@class, 'react-pdf__Page')]")
        self.file_close_button = self.browser.element("//div[contains(@class, 'Controls_closeContainer')]/button")
        self.share_screen_modal = self.browser.element(by.class_contains("ScreenShare_screenShareWrap_temp"))
        self.participant_container = Participant(
            root=self.browser.element(
                './/*[text()="Guest participant"]/ancestor::*[contains(@class,"ParticipantVideo_container")]'
            )
        )

    @report.step()
    def select_side_menu_by_name(self, name):
        self.browser.element(f'.//*[@data-testid="toggle-{name}-button"]').click()

    def disable_video(self):
        if self.video_button.matching(have.attribute("class").value_containing("UserVideoPreview_camEnabled")):
            self.video_button.click()


class EndSessionModal(Modal):
    def __init__(self, browser_instance: Browser = browser):
        super().__init__(browser_instance=browser_instance)
        self.end_for_all_button = self._container.element(
            './/*[contains(@class, "Button-module_button") and (text()="End for everyone")]'
        )


class SettingsMenu(MoreMenuThirdOption):
    def __init__(self):
        super().__init__(
            root=browser.element(by.class_contains("MobileActionsMenu_wrap")),
            open_menu_button_locator=by.class_contains("ToolbarButton_button"),
            opened_menu_locator=by.class_contains("MobileActionsMenu_menuWrap"),
            item_locator=by.class_starts_with("MobileActionsMenu_menuItemLabelWrap"),
        )

    @report.step
    def open_menu(self):
        self._container.hover()
        self.menu_items.first.should(be.visible)


class SessionRecordingModal(Modal):
    def __init__(self, browser_instance: Browser = browser):
        super().__init__(browser_instance=browser_instance)
        self.continue_button = self._container.element(
            './/*[contains(@class, "Button-module_button") and (text()="Continue")]'
        )


class MoreOptionsMenuModal(Modal):
    def __init__(self, browser_instance: Browser = browser):
        super().__init__(browser_instance=browser_instance)
        self.guest_link = self._container.element(by.class_starts_with("Input-module_input"))


class DocPickerModal(FloatingModal):
    def __init__(self, browser_instance: Browser = browser):
        super().__init__(browser_instance=browser_instance)
        self.file_input = self._container.element('.//*[@data-testid="file-input"]')
        self.close_doc_picker = self._container.element('[data-testid="file-upload-close-button"]')
        self.file_name = self._container.element('div[data-testid="uploaded-file-row-0"]')
        self.share_file_button = self._container.element('button[data-testid="share-tag"]')
