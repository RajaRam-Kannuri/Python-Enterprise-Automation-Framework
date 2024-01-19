import allure
import pytest
from selene import have

from test_data import IMAGES_PATH
from util import labels


@labels.ui
@pytest.mark.smokes
@allure.epic("Classroom")
@allure.feature("Smokes")
@allure.severity(allure.severity_level.CRITICAL)
class TestVirtualBackground:
    @staticmethod
    @allure.id("11547")
    @pytest.mark.parametrize("background_option", ["Blur my background", "Without effects"])
    def test_to_check_blur_background(instant_session, background_option):
        allure.dynamic.title(f"[UI][Smokes] Verify background option: '{background_option}'")
        instant_session.settings_menu.select_item_by_text("Background settings")
        while len(instant_session.background_images) > 3:
            instant_session.background_images[3].hover()
            instant_session.delete_custom_background.click()
        instant_session.background_images.should(have.size(3))
        instant_session.background_items.by(have.text(background_option))[0].click()
        instant_session.exit_option_button.click()
        instant_session.end_session_modal.end_for_all_button.click()

    @staticmethod
    @allure.id("11546")
    @allure.title("[UI][Smokes] Verify user can upload and delete a custom background")
    def test_to_check_custom_background(instant_session):
        with allure.step("Open background settings"):
            instant_session.settings_menu.select_item_by_text("Background settings")
            instant_session.background_items.by(have.text("Without effects"))[0].click()
            while len(instant_session.background_images) > 3:
                instant_session.background_images[3].hover()
                instant_session.delete_custom_background.click()
            instant_session.background_images.should(have.size(3))
            instant_session.background_items.by(have.text("Add custom background"))
        with allure.step("Upload a background image"):
            my_file = IMAGES_PATH / "constructor_tech.jpg"
            instant_session.upload_background_image.send_keys(str(my_file))
            instant_session.background_images.should(have.size(4))
            instant_session.upload_background_image.send_keys(str(my_file))
            instant_session.background_images.should(have.size(5))
            instant_session.background_items.by(have.text("Without effects"))[0].click()
        with allure.step("Delete all custom background"):
            while len(instant_session.background_images) > 3:
                instant_session.background_images[3].hover()
                instant_session.delete_custom_background.click()
            instant_session.side_menu_close_button.click()
        instant_session.exit_option_button.click()
        instant_session.end_session_modal.end_for_all_button.click()
