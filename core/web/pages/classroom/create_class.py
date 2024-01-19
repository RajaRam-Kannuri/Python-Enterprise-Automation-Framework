from selene import browser

from core.web.elements.dynamic.more_menu import MoreMenuThirdOption
from core.web.elements.static.modal import Modal
from core.web.pages.platform_base_page import PlatformBaseStaticPage
from util.web.assist.selene.extended import by


class CreatePage(PlatformBaseStaticPage):
    URL = "classroom/classrooms/create"

    def __init__(self):
        super().__init__(self.URL)
        self.icon_button = browser.element(by.class_contains("IconButton-module_small"))
        self.name_input = browser.element(by.class_contains("Input-module_input"))
        self.description_input = browser.element(by.class_contains("Textarea-module_textarea"))
        self.save_button = browser.element(by.text("Save and exit"))
        self.more_menu = MoreMenuThirdOption(root=browser.element(by.class_starts_with("ClassroomItem_item")))
        self.delete_confirmation_modal = DeleteConfirmationModal()


class DeleteConfirmationModal(Modal):
    def __init__(self):
        super().__init__()
        self.delete_button = browser.element(by.class_contains("Button-module_attention"))
