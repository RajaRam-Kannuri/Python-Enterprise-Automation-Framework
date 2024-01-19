from selene import have

from core.web.elements.base_element import BaseElement
from core.web.elements.dynamic.more_menu import MoreMenuWithSubMenu
from util.web.assist.allure import report
from util.web.assist.selene.extended import by


class SessionRole(BaseElement):
    """
    Represents a general role in the session.
    """

    def __init__(self, role_name, root):
        super().__init__()
        """
        Initialize a SessionRole instance.
        """
        self._container = root
        self.role = self._container.element(
            f'.//*[contains(@class ,"Accordion-module_title") and contains(text(),"{role_name}")]/ancestor::*[4]'
        )
        self.list_of_members = self.role.all(by.class_starts_with("UsersOfRole_wrap"))
        self.role_menu = MoreMenuWithSubMenu(root=self.role)
        self.moderator_menu = MoreMenuWithSubMenu(root=self.role)


class HostRole(SessionRole):
    def __init__(self, root):
        super().__init__(role_name="Host", root=root)


class ParticipantRole(SessionRole):
    def __init__(self, root):
        super().__init__(role_name="Participants", root=root)
        self.mute_icons = self.role.all(".//*[contains(@class, 'Item_mic')]")


class PresenterRole(SessionRole):
    def __init__(self, root):
        super().__init__(role_name="Presenters", root=root)


class ModeratorRole(SessionRole):
    def __init__(self, root):
        super().__init__(role_name="Moderator", root=root)


class Participant(BaseElement):
    """
    Represents a participant in the session.
    """

    def __init__(self, root):
        super().__init__()
        self._container = root
        self.participant_pin_icon = self._container.element(by.xpath('.//button//*[contains(@name,"Pin")]'))

    @report.step
    def pin(self):
        return self._container.element(by.class_contains("ParticipantVideo_putOnStageBtn")).click()

    @report.step
    def should_be_pinned(self):
        return self.participant_pin_icon.should(have.attribute("name", "PinVerticalBoldStroke"))

    @report.step
    def should_be_unpinned(self):
        return self.participant_pin_icon.should(have.attribute("name", "PinDiagonalBoldStroke"))
