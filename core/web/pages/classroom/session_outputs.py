from core.web.pages.classroom.session_roles import HostRole, ParticipantRole, PresenterRole
from core.web.pages.platform_base_page import PlatformBaseStaticPage
from util.web.assist.selene.extended import by


class SessionOutputsPage(PlatformBaseStaticPage):
    URL = "classroom/outputs"

    def __init__(self):
        super().__init__(self.URL)
        self.host = HostRole(root=self.browser.element(by.class_starts_with("ParticipantsList_wrap")))
        self.participants = ParticipantRole(root=self.browser.element(by.class_starts_with("ParticipantsList_wrap")))
        self.presenters = PresenterRole(root=self.browser.element(by.class_starts_with("ParticipantsList_wrap")))
        self.description_list = self.browser.all(by.class_starts_with("Caption_caption"))
        self.open_session = self.browser.element(by.class_contains("OutputItem_item"))
