from datetime import datetime, timedelta

import allure
import pytest
from selene import be, have, query

from core.web.pages.classroom.create_session import CreateSessionPage
from core.web.pages.classroom.instant_session import InstantSessionPage
from core.web.pages.classroom.online_session import OnlineSessionPage
from util import labels
from util.random import random_text


@labels.ui
@pytest.mark.smokes
@allure.epic("Classroom")
@allure.feature("Smokes")
@allure.severity(allure.severity_level.CRITICAL)
class TestSession:
    @staticmethod
    @allure.id("9913")
    @allure.title("[UI][Smoke] Check creation of session with class")
    def test_create_scheduled_session_with_class(session_page):
        session_page.create_session_dropdown.select_item_by_text("Schedule session")
        create_session = CreateSessionPage()
        start_time = create_session.round_time(datetime.now() + timedelta(days=1, hours=2))
        end_time = create_session.round_time(datetime.now() + timedelta(days=1, hours=3, minutes=15))

        create_session.class_selection_dropdown.select_item_by_index(1)
        session_name = create_session.class_selection_dropdown.input.get(query.value)
        create_session.session_date_input.set_date(datetime.now().date() + timedelta(days=1))
        create_session.set_session_time(start=start_time, end=end_time)
        create_session.displayed_time_duration.should(have.text("75 minutes session"))
        create_session.guest_link_toggle_checkbox.click()
        create_session.guest_alert_message.should(be.hidden)

        create_session.create_session_button.click()
        create_session.page_title.should(have.text(session_name))

    @staticmethod
    @allure.id("9911")
    @allure.title("[UI][Smoke] Check creation of session without class")
    def test_create_scheduled_session_without_class(session_page):
        session_page.create_session_dropdown.select_item_by_text("Schedule session")
        create_session = CreateSessionPage()
        start_time = create_session.round_time(datetime.now() + timedelta(days=1, hours=6, minutes=30))
        end_time = create_session.round_time(datetime.now() + timedelta(days=1, hours=7, minutes=15))

        session_name = random_text(10)
        create_session.name_form.fill_with_text(session_name)
        create_session.session_date_input.set_date(datetime.now().date() + timedelta(days=1))
        create_session.description_form.fill_with_text(random_text(30))
        create_session.set_session_time(start=start_time, end=end_time)
        create_session.displayed_time_duration.should(have.text("45 minutes session"))
        create_session.guest_link_toggle_checkbox.click()
        create_session.guest_alert_message.should(be.hidden)
        create_session.upload_session_file("demo_file")

        create_session.create_session_button.click()
        create_session.page_title.should(have.text(session_name))

    @staticmethod
    @allure.id("10461")
    @allure.title("[UI][Smoke] Check update of scheduled session")
    def test_update_session_creation(session_creation_page):
        session_creation_page.name_form.fill_with_text("demo test class")
        session_creation_page.session_date_input.set_date(datetime.now().date() + timedelta(days=2))
        session_creation_page.set_session_time(
            start=session_creation_page.round_time(datetime.now() + timedelta(days=1, minutes=30)),
            end=session_creation_page.round_time(datetime.now() + timedelta(days=1, hours=1, minutes=15)),
        )
        session_creation_page.description_form.fill_with_text("This is a demo test class")
        session_creation_page.guest_link_toggle_checkbox.click()
        session_creation_page.guest_session_link.should(be.hidden)
        session_creation_page.upload_session_file("demo_file")
        session_creation_page.update_session_button.click()

    @staticmethod
    @allure.id("9914")
    @allure.title("[UI][Smoke] Check creation and deletion of scheduled session")
    def test_instant_session_creation_and_deletion(session_page):
        session_page.create_session_dropdown.select_item_by_text("Start instant session")
        instant_session = InstantSessionPage()
        instant_session.start_session_button.should(have.text("Start the session")).click()
        instant_session.participant_video.should(be.visible)
        instant_session.exit_option_button.click()
        instant_session.end_session_modal.end_for_all_button.click()
        instant_session.confirmation_text.should(have.text("Session is ended"))

    @staticmethod
    @allure.id("9929")
    @allure.title("[UI][Smoke] Check creation of session as a host")
    def test_create_session_as_host(session_creation_page):
        session_name = session_creation_page.page_title.get(query.text)
        session_creation_page.update_session_button.click()
        session_page = OnlineSessionPage()
        session_page.session_search_input.type(session_name)
        session_page.session_table.get_row_by_cell_value(
            column_name="Session name", value=session_name
        ).start_session_button.click()
        session = InstantSessionPage()
        session.background_image_button.click()
        session.blur_background_image.click()
        session.side_menu_close_button.click()
        session.elements_enabled.should(have.size(2))
        session.start_session_button.click()
        session.participant_video.should(be.visible)
        session.exit_option_button.click()
        session.end_session_modal.end_for_all_button.click()
