import allure
import pytest
from selene import be, have

from core.web.pages.classroom.instant_session import InstantSessionPage
from test_data import FILES_PATH
from util import labels


@labels.ui
@pytest.mark.smokes
@allure.epic("Classroom")
@allure.feature("Smokes")
@allure.severity(allure.severity_level.CRITICAL)
class TestPresenterRole:
    @staticmethod
    @allure.id("9921")
    @allure.title("[UI][Smoke] Check assign of presenter role")
    def test_assign_presenter_role(guest_session):
        guest_session.participant_video.should(be.visible)

        session = InstantSessionPage()
        session.participant_list_button.click()
        session.participant_list_items.should(have.size(2))
        session.presenter.role_menu.select_menu_and_submenu_by_text("Roles", "Make a Presenter")
        session.toast.text.should(be.visible).with_(timeout=1).should(have.text("Guest participant is now a Presenter"))
        session.presenter.list_of_members.filtered_by(have.text("Guest participant")).should(have.size(1))
        session.exit_option_button.click()
        session.end_session_modal.end_for_all_button.click()

    @staticmethod
    @allure.id("9923")
    @allure.title("[UI][Smoke] Verify file sharing as presenter")
    def test_share_file_as_presenter(setup_presenter_role):
        session, guest_session = setup_presenter_role
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
    @allure.id("9928")
    @allure.title("[UI][Smoke] Verify screen sharing as presenter")
    def test_share_screen_as_presenter(setup_presenter_role):
        session, guest_session = setup_presenter_role
        guest_session.content_dropdown.select_item_by_text("Your screen")
        guest_session.share_screen_modal.should(be.visible)
        guest_session.participant_alignment_indicator.should(be.visible)
        session.share_screen_modal.should(be.visible)
        guest_session.content_dropdown.select_item_by_text("Your screen")
        guest_session.share_screen_modal.should(be.not_.visible)
        session.exit_option_button.click()
        session.end_session_modal.end_for_all_button.click()
