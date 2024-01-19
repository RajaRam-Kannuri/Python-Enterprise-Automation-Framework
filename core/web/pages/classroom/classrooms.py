from selene import browser

from core.web.pages.platform_base_page import PlatformBaseStaticPage, SideMenu
from util.web.assist.selene.extended import by


class ClassRoomPage(PlatformBaseStaticPage):
    URL = "classroom/classrooms"

    def __init__(self):
        super().__init__(self.URL)
        self.class_view = browser.element(by.class_contains("ClassroomItem_item"))
        self.create_class_button = browser.element(by.text("Create a class"))
        self.open_button = browser.element(by.text("Open"))
        self.get_class_title = browser.element(by.class_contains("ClassroomItem_title"))
        self.control_sidebar = ClassRoomSideMenu()


class ClassRoomSideMenu(SideMenu):
    MENU_LOCATOR = ".//li//div//button"

    def __init__(self):
        super().__init__()
