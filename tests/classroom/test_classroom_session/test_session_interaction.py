import time

import allure
import pytest
from selene import be, browser, have

from core.models.lms.lms_user import User
from core.web.pages.classroom.instant_session import InstantSessionPage
from util import labels


@labels.ui
@pytest.mark.smokes
@allure.epic("Classroom")
@allure.feature("Smokes")
@allure.severity(allure.severity_level.CRITICAL)
class TestClassroomSessionInteractions:
    @staticmethod
    @allure.id("9916")
    @allure.title("[UI][Smoke] Check if guest can join session")
    def test_guest_can_join_session(host_session, second_browser):
        second_browser.open(host_session)
        guest_session_page = InstantSessionPage(second_browser)
        guest_session_page.participant_name_input.set_value("Guest participant")
        guest_session_page.start_session_button.should(have.text("Enter the session")).click()
        guest_session_page.participant_video.should(be.visible)
        guest_session_page.participant_list_button.click()
        guest_session_page.participant_list_items.should(have.size(2))

    @staticmethod
    @allure.id("9925")
    @allure.title("[UI][Smoke] Check if host can mute all participants")
    def test_host_can_mute_all_participants(host_session, second_browser, tenant_user: User):
        MUTE_DISABLED_COLOR = "#D4083B"
        second_browser.open(host_session)
        guest_page = InstantSessionPage(second_browser)
        guest_page.participant_name_input.set_value("test participant")
        guest_page.disable_video()
        guest_page.start_session_button.should(be.visible).click()
        session_page = InstantSessionPage()
        session_page.participant_list_button.click()
        session_page.toast.text.should(be.visible).with_(timeout=1).should(
            have.text("test participant has joined the session")
        )
        session_page.toast.close()
        session_page.participant_list_items.should(have.size(2))
        session_page.presenter.role_menu.select_menu_and_submenu_by_text("Roles", "Make a Participant")
        session_page.toast.text.should(be.visible).with_(timeout=1).should(
            have.text("test participant is now a Participant")
        )
        session_page.toast.close()
        session_page.participant.moderator_menu.select_menu_and_submenu_by_text("Moderation", "Mute All")
        session_page.toast.text.should(be.visible).with_(timeout=1).should(
            have.text(f"{tenant_user.first_name} {tenant_user.last_name} muted all participants")
        )
        session_page.participant.mute_icons.filtered_by(have.attribute(name="fill", value=MUTE_DISABLED_COLOR)).should(
            have.size(1)
        )

    @staticmethod
    @allure.id("11548")
    @allure.title("[UI][Smoke] Verify Sharing guest link from session")
    def test_verify_guest_link(host_session, second_browser):
        second_browser.open(host_session)
        guest_session = InstantSessionPage(second_browser)
        guest_session.participant_name_input.set_value("Guest participant")
        guest_session.start_session_button.click()

        browser.should(have.url(host_session))
        guest_session.participant_list_button.click()
        guest_session.participant_list_items.should(have.size(2))

    @staticmethod
    @allure.id("10755")
    @allure.title("[UI][Smoke] Verify pin and unpin of participant")
    def test_pin_participant(guest_session):
        guest_session.participant_video.should(be.visible).hover()
        guest_session.participant_container.pin()
        guest_session.participant_container.should_be_pinned()
        guest_session.participant_alignment_indicator.should(be.visible)
        guest_session.participant_container.pin()
        guest_session.participant_container.should_be_unpinned()
        guest_session.participant_alignment_indicator.should(be.not_.visible)
