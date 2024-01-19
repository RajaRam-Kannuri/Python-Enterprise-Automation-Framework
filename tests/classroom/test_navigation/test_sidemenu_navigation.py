import allure
import pytest
from selene import have

from core.web.pages.classroom.classrooms import ClassRoomPage
from util import labels


@labels.ui
@pytest.mark.smokes
@allure.epic("Classroom")
@allure.feature("Smokes")
@allure.severity(allure.severity_level.CRITICAL)
class TestNavigationDemo:
    test_data = [
        ("1931", "[UI][Smoke] Check navigation to content libraries", None, "Content libraries"),
        ("1932", "[UI][Smoke] Check navigation to quizzes", "Quizzes", "Quizzes"),
        ("1933", "[UI][Smoke] Check navigation to questions", "Questions", "Questions"),
        ("1934", "[UI][Smoke] Check navigation to pools", "Pools", "Pools"),
        ("1935", "[UI][Smoke] Check navigation to labs", "Labs", "Labs"),
        ("1936", "[UI][Smoke] Check navigation to classes", "Classes", "Classes"),
        ("1937", "[UI][Smoke] Check navigation to session output", "Session outputs", "Meeting rooms"),
    ]

    @staticmethod
    @pytest.mark.parametrize("test_id, title, submenu_name, expected_text", test_data)
    def test_navigation(users_page, test_id, title, submenu_name, expected_text):
        allure.dynamic.id(test_id)
        allure.dynamic.title(title)

        users_page.control_sidebar.open_menu_by_name(menu_name="Content libraries", submenu_name=submenu_name)
        users_page.page_title.should(have.text(expected_text))

        if submenu_name == "Classes":
            ClassRoomPage().should_be_opened().page_title.should(have.text(expected_text))
