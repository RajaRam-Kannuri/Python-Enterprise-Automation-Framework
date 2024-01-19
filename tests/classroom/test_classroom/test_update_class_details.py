import allure
import pytest
from selene import be, have

from core.web.pages.classroom.classroom_setup import ClassroomSetupPage
from core.web.pages.classroom.classrooms import ClassRoomPage
from test_data import FILES_PATH, IMAGES_PATH
from util import labels
from util.random import random_text


@labels.ui
@pytest.mark.smokes
@allure.epic("Classroom")
@allure.feature("Smokes")
@allure.severity(allure.severity_level.CRITICAL)
class TestUpdateClassroom:
    @staticmethod
    @allure.id("10354")
    @allure.title("[UI][Smokes] Check updation of classroom details")
    def test_update_classroom_details(classroom):
        class_page = ClassRoomPage().should_be_opened()
        class_page.open_button.click()
        setup_page = ClassroomSetupPage()
        setup_page.name_form.fill_with_text(random_text(n=10))
        setup_page.description_input_field.set_value(random_text(n=143))

        my_image = IMAGES_PATH / "constructor_tech.jpg"
        setup_page.file_input.send_keys(str(my_image))
        setup_page.check_image_visibility.should(be.visible)
        setup_page.save_button.click()

        class_page.page_title.should(have.exact_text("Classes"))

    @staticmethod
    @allure.id("10460")
    @allure.title("[UI][Smokes] Check upload of classroom file")
    def test_upload_classroom_file(classroom):
        class_page = ClassRoomPage()
        class_page.open_button.click()

        class_page.control_sidebar.open_menu_by_name(classroom)
        setup_page = ClassroomSetupPage()

        my_file = FILES_PATH / "demo_file.pdf"
        setup_page.file_input.should(be.present).send_keys(str(my_file))
        setup_page.table.all_rows_should_have_value_in_column(column_name="Name", value="demo_file.pdf")
        setup_page.table.rows.should(have.size(1))
        setup_page.save_button.click()

        class_page.page_title.should(have.exact_text("Classes"))
