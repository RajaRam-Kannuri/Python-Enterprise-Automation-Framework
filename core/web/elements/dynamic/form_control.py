import json
import time
from datetime import datetime

from selene import have, query
from selene.core.entity import Element
from selenium.webdriver import Keys

from core.web.elements.base_element import BaseElement
from util.web.assist.allure import report
from util.web.assist.selene.extended import by


class FormControl(BaseElement):
    """
    Form control element is an element that has a label and an input field and can show some error messages.
    This element can be defined by a label or by a placeholder.
    """

    by_placeholder_locator_stub = (
        './/*[@class[contains(., "FormControl-module")] and .//input[@placeholder="{by_placeholder}"]]'
    )
    by_label_locator_stub = None
    error_message_locator = by.class_starts_with("FormControl-module_error")
    input_locator = "input"

    def __init__(self, root: Element, by_placeholder: str = None, by_label: str = None):
        super().__init__()
        if by_placeholder and by_label:
            raise ValueError("you can not use 'by_placeholder' and 'by_label' attributes at the same time")
        self.description_text = by_placeholder or by_label
        if by_placeholder:
            self._container: Element = root.element(
                self.by_placeholder_locator_stub.format(by_placeholder=by_placeholder)
            )
        elif by_label:
            self._container: Element = root.element(self.by_label_locator_stub.format(by_label=by_label))
        self.label = self._container.element("label")
        self.input: Element = self._container.element(self.input_locator)
        self.error_field: Element = self._container.element(self.error_message_locator)

    def __str__(self):
        return self.description or f'{self.__class__.__name__}:"{self.description_text}"'


class OldFormControl(FormControl):
    error_message_locator = './/*[@role="alert"]'
    by_label_locator_stub = './/*[contains(@class, "v-input__control") and .//label[text()="{by_label}"]]'
    input_locator = './/*[local-name() = "input" or local-name() = "textarea"]'


class TextFormControl(FormControl):
    @report.step
    def clear(self):
        self.input.clear()

    @report.step
    def fill_with_text(self, text):
        self.clear()
        self.input.type(text)


class OldTextFormControl(TextFormControl, OldFormControl):
    @report.step
    def clear(self):
        input_length = len(self.input.get(query.attribute("value")))

        for _ in range(input_length):
            self.input.send_keys(Keys.BACKSPACE)
        return self


class OldCheckboxForm(OldFormControl):
    @property
    def is_checked(self):
        return json.loads(self.input.get(query.attribute("aria-checked")))

    def make_checked(self):
        if not self.is_checked:
            self.input.click()

    def should_be_checked(self):
        self.input.should(have.attribute("aria-checked").value("true"))


class BaseFormControl(TextFormControl):
    input_locator = './/*[local-name() = "input" or local-name() = "textarea"]'

    @report.step
    def clear(self):
        while len(self.input.get(query.value)) != 0:
            input_length = len(self.input.get(query.value))
            for _ in range(input_length):
                self.input.send_keys(Keys.BACKSPACE)
            time.sleep(0.2)


class DateFormControl(BaseFormControl):
    INPUT_DATE_FORMAT = "%d-%m-%Y"
    input_locator = 'input[type="date"]'

    @report.step
    def set_date(self, date_object=None):
        if date_object is None:
            date_object = datetime.now().date()
        formatted_date = date_object.strftime(self.INPUT_DATE_FORMAT)
        self.fill_with_text(formatted_date)


class ClassroomFormControl(BaseFormControl):
    by_label_locator_stub = './/*[@class[contains(., "FormControl-module")] and .//label[text() = "{by_label}"]]'


class LmsFormControl(BaseFormControl):
    by_label_locator_stub = (
        '//*[contains(@class, "UiField-module") or contains(@class, "UiInput-module")]['
        './/label/span[text() = "{by_label}"]]'
    )
    error_message_locator = '//*[@class[contains(., "UiField-module_message")]]'
    input_locator = './/*[(local-name() = "input" and @type="text") or local-name() ="textarea"]'

    @report.step
    def type_one_by_one(self, text):
        for char in text:
            self.input.send_keys(char)
        return self
