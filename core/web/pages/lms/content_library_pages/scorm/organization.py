import mimetypes
import re
import time
from pathlib import Path

from selene import be, browser, have, query
from selenium.webdriver import ActionChains

from core.web.elements.dynamic.dropdowns import DropdownWithInput
from core.web.elements.dynamic.form_control import LmsFormControl
from core.web.elements.dynamic.frame import Frame
from core.web.elements.dynamic.more_menu import LibrarySettingsMoreMenu
from core.web.elements.static.modal import Modal
from core.web.elements.static.toast import NewToastItem
from core.web.pages.lms.lms_base_page import LmsBasePage
from core.web.pages.platform_base_page import PlatformBaseDynamicPage
from settings import settings
from test_data import FILES_PATH
from util.web.assist.allure import report
from util.web.assist.selene.extended import by
from util.web.assist.selene.extended.commands import upload_file_with_drag_and_drop


class OrganizationPage(Frame, PlatformBaseDynamicPage, LmsBasePage):
    IMAGE_VIEW_TIMEOUT: float = 2.0

    def __init__(self):
        super().__init__(
            iframe=browser.element('iframe[id="tooliframe"]'),
            url_template="teach/content-libraries/{scorm_library_id}/lti?toolUrl={base_url}launch",
        )
        self.file_input = browser.element('input[type="file"]')
        self.toast_message = NewToastItem()
        self.cancel_button = browser.element("//button[contains(text(),'Cancel Upload')]")
        self.drop_area = browser.element("//*[contains(text(), 'Drag and drop')]")
        self.select_file_button = browser.element("//button[contains(text(),'Select file')]")
        self.description_input = browser.element("textarea[name='description']")
        self.save_button = browser.element("//button[@type='submit' and text()='Save']")
        self.package_preview = browser.element(by.class_starts_with("PreviewPackage_packageName"))
        self.title_form = LmsFormControl(root=browser.element(by.class_contains("EditorForm_column")), by_label="Title")
        self.code_form = LmsFormControl(
            root=browser.element(by.class_contains("EditorForm_column")), by_label="Code or ID"
        )
        self.description_form = LmsFormControl(
            root=browser.element(by.class_contains("EditorForm_column")), by_label="Description"
        )
        self.state_dropdown = DropdownWithInput(root=browser.element(by.class_contains("Select-module_wrapper")))
        self.scorm_page_link = browser.element("//a[contains(text(),'SCORM')]")
        self.edit_image_crop_modal = EditImageCropModal()
        self.image_preview = browser.element("img[alt='Preview']")
        self.spinner = browser.element('//*[@data-testid="spinner"]')
        self.image_info = browser.element(by.class_starts_with("ImageInfo-module_info"))
        self.paste_link_field = browser.element("//div[contains(@class,'ImageUploader-module_fileUrlInput')]//input")
        self.link_form = LmsFormControl(
            root=browser.element(by.class_contains("EditorForm_column")),
            by_label="Paste a link to an external cover " "image",
        )
        self.delete_image_button = browser.element("//button[contains(text(),'Delete')]")
        self.image_original_size = browser.element(by.class_starts_with("ImageInfo-module_size"))
        self.edit_image_button = browser.element("//button[contains(text(),'Edit')]")
        self.edit_modal = browser.element(by.id("image-cropper-modal"))
        self.settings = LibrarySettingsMoreMenu(
            root=browser.element(by.class_contains("UiCollapsible-module_container"))
        )

    @staticmethod
    def _drag_and_drop_file(file_path: Path):
        # Prepare file object in Python
        file_data = file_path.read_bytes()
        file_name = file_path.name

        mime_type, _ = mimetypes.guess_type(file_name)
        if mime_type is None:
            mime_type = "application/octet-stream"  # Default to binary if MIME type cannot be determined

        file_object: dict = {"data": file_data, "name": file_name, "type": mime_type}
        return upload_file_with_drag_and_drop(file_object["data"], file_object["name"], file_object["type"])

    @report.step
    def upload_file(self, file_path, use_drag_and_drop=False):
        if use_drag_and_drop:
            self.drop_area.should(be.visible)
            self.drop_area.perform(self._drag_and_drop_file(file_path))
        else:
            self.file_input.send_keys(str(file_path))

    @report.step
    def generate_new_code(self, package_name: str):
        expected_message = f'Successfully uploaded your SCORM package "{package_name}"'

        with self.make_active() as create_frame:
            create_frame.upload_file(file_path=FILES_PATH / package_name, use_drag_and_drop=False)
            create_frame.toast_message.message.should(have.text(expected_message).and_(be.visible))
            create_frame.package_preview.should(be.visible).should(have.text(package_name))
            code = create_frame.code_form.input.get(query.attribute("value"))
            create_frame.description_input.type("Autotest description")
            create_frame.save_button.click()

        return code

    @report.step
    def save(self):
        with self.make_active() as edit_frame:
            edit_frame.save_button.click()

    @report.step
    def wait_for_spinner_to_hide(self):
        if self.spinner.with_(timeout=settings.recheck_timeout).wait_until(be.visible):
            self.spinner.should(be.hidden)

    @report.step
    def add_image(self, file_path: Path, use_drag_and_drop: bool = False):
        with self.make_active() as edit_frame:
            edit_frame.upload_file(file_path=file_path, use_drag_and_drop=use_drag_and_drop)
            edit_frame.wait_for_spinner_to_hide()
            edit_frame.edit_image_crop_modal.header.should(have.text("Edit image crop"))
            edit_frame.wait_for_picture_to_be_ready()
            edit_frame.edit_image_crop_modal.ok_button.click()
            edit_frame.image_preview.should(be.present)
            edit_frame.save_button.click()

    @report.step
    def delete_image(self):
        with self.make_active() as edit_frame:
            edit_frame.delete_image_button.click()

    @report.step
    def get_image_external_link(self):
        with self.make_active() as edit_frame:
            image_link = edit_frame.image_preview.get(query.attribute("src"))
            self.scorm_page_link.click()
        return image_link

    @report.step
    def get_image_width_and_height(self):
        with self.make_active() as edit_frame:
            edit_frame.image_original_size.should(have.text("Original"))
            size = edit_frame.image_original_size.get(query.text)
            width, height = map(int, size.split(" ")[1].split("x"))
        return width, height

    @report.step
    def wait_for_picture_to_be_ready(self):
        # TODO: After fix of https://youtrack.constr.dev/issue/ALMS-5678/Edit-Image-Crop-Modal-OK-Button-Enabled-Before
        #  -Image-Load sleep will be replaced
        time.sleep(1)

    @report.step
    def open_edit_image_crop(self):
        with self.make_active() as edit_frame:
            edit_frame.wait_for_spinner_to_hide()
            edit_frame.edit_image_button.click()
            edit_frame.edit_image_crop_modal.header.should(have.text("Edit image crop"))
            edit_frame.wait_for_picture_to_be_ready()

    @report.step
    def adjust_setting(self, setting_name, check=True):
        with self.make_active() as edit_frame:
            edit_frame.wait_for_spinner_to_hide()
            edit_frame.settings.open_menu()
            setting_control = edit_frame.settings.get_setting_control(setting_name)
            if check:
                setting_control.modify_checkbox(check)
            else:
                setting_control.modify_checkbox(check)


class EditImageCropModal(Modal):
    def __init__(self):
        super().__init__()
        self.ok_button = self.footer.element(by.text("OK"))
        self.cancel_button = self.footer.element(by.text("Cancel"))
        self.picture = self.section.element(
            by.xpath(".//div[contains(@class,'ImageCropper-module_cropperContainer')]/div/img[@alt='picture']")
        )
        self.zoom_in_button = self.section.element("button[aria-label='Zoom in']")
        self.zoom_out_button = self.section.element("button[aria-label='Zoom out']")
        self.move_button = self.section.element("button[aria-label='Move']")
        self.crop_box = self.section.element(".cropper-crop-box")
        self.reset_button = self.section.element("button[aria-label='Reset']")
        self.crop_button = self.section.element("button[aria-label='Crop']")
        self.cropper_point = self.section.element("[data-cropper-action='nw']")

    @report.step
    def move_image(self, x_offset: int):
        self.move_button.click()
        ActionChains(browser.driver).click_and_hold(self.crop_box.locate()).move_by_offset(
            x_offset, 0
        ).release().perform()

    @report.step
    def get_cropbox_transform_value(self):
        style = self.crop_box.get(query.attribute("style"))
        translate_x = re.findall(r"translateX\((.+?)\)", style)[0]
        value = translate_x.replace("px", "")

        return value

    @report.step
    def crop_image(self, x_offset: int, y_offset: int):
        self.crop_button.click()
        ActionChains(browser.driver).click_and_hold(self.cropper_point()).move_by_offset(
            x_offset, y_offset
        ).release().perform()
