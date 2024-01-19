import datetime

import allure
import pytest
from assertpy import assert_that
from selene import be, have, query

from core.web.pages.classroom.session_details import SessionDetailsPage
from core.web.pages.classroom.session_outputs import SessionOutputsPage
from util import labels


@labels.ui
@pytest.mark.smokes
@allure.epic("Classroom")
@allure.feature("Smokes")
@allure.severity(allure.severity_level.CRITICAL)
class TestSessionOutput:
    @staticmethod
    @allure.id("9930")
    @allure.title("[UI][Smoke] Check session outputs")
    def test_session_output(manage_session):
        start_time, end_time, session_page = manage_session

        session_page.control_sidebar.open_menu_by_name(menu_name="Content libraries", submenu_name="Session outputs")
        session_page.page_title.should(have.text("Meeting rooms"))

        outputs = SessionOutputsPage().open()
        outputs.open_session.should(be.visible).click()

        output_details = SessionDetailsPage()
        output_details.head_navigation.click_item(name="Description")
        output_details.date_and_time.should(have.text("Date and time"))
        start_hour = output_details.remove_leading_zeros(start_time.strftime("%H"))
        end_hour = output_details.remove_leading_zeros(end_time.strftime("%H"))
        time_in_string = f"{start_hour}:{start_time.strftime('%M')} — {end_hour}:{end_time.strftime('%M')}"

        output_details.date_and_time.should(
            have.text((datetime.datetime.now()).strftime("%d-%m-%Y")).and_(have.text(time_in_string))
        )
        output_details.duration.should(have.text("Duration"))
        actual_duration = output_details.parse_to_timedelta(
            output_details.duration.get(query.text).replace("Duration\n", "")
        )
        expected_duration = datetime.timedelta(seconds=round(abs(end_time - start_time).total_seconds()))

        assert_that(expected_duration.total_seconds()).is_close_to(actual_duration.total_seconds(), 1)

        output_details.head_navigation.click_item(name="Participants")
        outputs.host.list_of_members.should(have.size(1))
