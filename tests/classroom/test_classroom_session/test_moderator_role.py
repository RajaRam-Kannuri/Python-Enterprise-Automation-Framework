import allure
import pytest
from selene import be, have

from core.web.pages.classroom.instant_session import InstantSessionPage
from core.web.pages.classroom.session_details import SessionDetailsPage
from core.web.pages.classroom.session_outputs import SessionOutputsPage
from test_data import FILES_PATH
from util import labels


@labels.ui
@pytest.mark.smokes
@allure.epic("Classroom")
@allure.feature("Smokes")
@allure.severity(allure.severity_level.CRITICAL)
class TestModeratorRole:
    @staticmethod
    @allure.id("9920")
    @allure.title("[UI][Smoke] Check assign of moderator role")
    def test_assign_moderator_role(guest_session):
        guest_session.participant_video.should(be.visible)

        session = InstantSessionPage()
        session.participant_list_button.click()
        session.participant_list_items.should(have.size(2))
        session.presenter.role_menu.select_menu_and_submenu_by_text("Roles", "Make a Moderator")
        session.toast.text.should(be.visible).with_(timeout=1).should(have.text("Guest participant is now a Moderator"))

        session.moderator.list_of_members.filtered_by(have.text("Guest participant")).should(have.size(1))
        session.exit_option_button.click()
        session.end_session_modal.end_for_all_button.click()

    @staticmethod
    @allure.id("9926")
    @allure.title("[UI][Smoke] Verify kick participant as moderator")
    def test_kick_participant_by_moderator(setup_moderator_role, second_guest):
        session, guest_session = setup_moderator_role
        guest_session.select_menu_by_name("Participants list")
        guest_session.participant_list_items.should(have.size(3))
        guest_session.presenter.moderator_menu.select_menu_and_submenu_by_text("Moderation", "Kick participant")
        guest_session.toast.text.should(have.text("Guest participant kicked Third participant"))
        guest_session.participant_list_items.should(have.size(2))
        session.toast.text.should(have.text("Guest participant kicked Third participant"))
        session.exit_option_button.click()
        session.end_session_modal.end_for_all_button.click()

    @staticmethod
    @allure.id("9924")
    @allure.title("[UI][Smoke] Verify file sharing as moderator")
    def test_share_file_as_moderator(setup_moderator_role):
        session, guest_session = setup_moderator_role
        guest_session.content_dropdown.select_item_by_text("Files")
        my_file = FILES_PATH / "demo_file.pdf"
        guest_session.doc_picker_modal.file_input.should(be.present).send_keys(str(my_file))
        guest_session.doc_picker_modal.file_name.should(be.present).should(have.text("demo_file.pdf"))
        guest_session.doc_picker_modal.share_file_button.click()
        guest_session.doc_picker_modal.close_doc_picker.click()
        guest_session.file_preview.should(be.visible)
        guest_session.file_close_button.click()
        session.exit_option_button.click()
        session.end_session_modal.end_for_all_button.click()

    @staticmethod
    @allure.id("9925")
    @allure.title("[UI][Smoke] Verify screen sharing as moderator")
    def test_share_screen_as_moderator(setup_moderator_role):
        session, guest_session = setup_moderator_role
        guest_session.content_dropdown.select_item_by_text("Your screen")
        guest_session.share_screen_modal.should(be.visible)
        guest_session.participant_alignment_indicator.should(be.visible)
        session.share_screen_modal.should(be.visible)
        guest_session.content_dropdown.select_item_by_text("Your screen")
        guest_session.share_screen_modal.should(be.not_.visible)
        session.exit_option_button.click()
        session.end_session_modal.end_for_all_button.click()

    @staticmethod
    @allure.id("9922")
    @allure.title("[UI][Smoke] Verify recording as moderator")
    def test_recording_as_moderator(setup_moderator_role):
        session, guest_session = setup_moderator_role
        guest_session.start_record_button.click()
        guest_session.recording_modal.continue_button.click()
        initiative_message = "Guest participant initiated session recording. It will start in a moment."
        guest_session.toast.text.should(have.text(initiative_message))
        session.toast.text.should(have.text(initiative_message))
        guest_session.toast.text.should(have.text("Recording is started."))
        session.toast.text.should(have.text("Recording is started."))
        guest_session.stop_record_button.click()
        guest_session.toast.text.should(have.text("Recording has stopped by ."))
        session.toast.text.should(have.text("Recording has stopped by ."))
        session.exit_option_button.click()
        session.end_session_modal.end_for_all_button.click()

        outputs = SessionOutputsPage().open()
        outputs.open_session.click()
        SessionDetailsPage().recording_player.should(be.visible)
