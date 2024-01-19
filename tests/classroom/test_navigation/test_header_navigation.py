import allure
import pytest
from selene import have

from util import labels


@labels.ui
@pytest.mark.smokes
@allure.epic("Classroom")
@allure.feature("Smokes")
@allure.severity(allure.severity_level.CRITICAL)
class TestHeaderNavigation:
    @staticmethod
    @allure.id("1961")
    @allure.title("[UI][Smokes] Check session header navigation to Rooms")
    def test_online_session_header_navigation(session_page):
        session_page.main_header.click_item(name="Rooms")
        session_page.page_title.should(have.text("Meeting rooms"))

    @staticmethod
    @allure.id("8956")
    @pytest.mark.parametrize("header_text, title", [("Classes", "Classes"), ("Session outputs", "Meeting rooms")])
    @allure.title("[UI][Smokes] Check content libraries header navigation")
    def test_content_library_header_navigation(content_page, header_text, title):
        content_page.main_header.click_item(name=header_text)
        content_page.page_title.should(have.text(title))
