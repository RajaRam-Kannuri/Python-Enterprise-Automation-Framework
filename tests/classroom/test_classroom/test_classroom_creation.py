import allure
import pytest
from selene import be, have

from core.web.pages.classroom.create_class import CreatePage
from util import labels
from util.random import random_string


@labels.ui
@pytest.mark.smokes
@allure.epic("classroom")
@allure.feature("Smokes")
@allure.severity(allure.severity_level.CRITICAL)
class TestClassroom:
    @staticmethod
    @allure.id("9912")
    @allure.title("[UI][Smoke] Check creation and deletion of classroom")
    def test_create_and_delete_classroom(class_page):
        class_name = random_string(min_length=20, prefix="Demo Class")

        class_page.create_class_button.click()
        create_class_page = CreatePage().should_be_opened()
        create_class_page.name_input.type(class_name)
        create_class_page.description_input.type(
            "This is a small demo virtual lab that will give you the idea how it works for the learner."
        )
        create_class_page.save_button.click()

        class_page.class_view.element(".//h3").should(be.visible).should(have.text(class_name))

        create_class_page.more_menu.select_item_by_text("Delete")
        create_class_page.delete_confirmation_modal.delete_button.click()
