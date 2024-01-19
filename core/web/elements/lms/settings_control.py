from selene import be, have

from core.web.elements.base_element import BaseElement


class SettingsControl(BaseElement):
    def __init__(self, container, setting_name):
        super().__init__()
        self._container = container
        self._setting_name = setting_name
        self.checkbox = self._container.element(
            f"//div[text()='{self._setting_name}']/ancestor::div[starts-with(@class,'ScormSettings_line')]//input[@type='checkbox']"
        )

        self.tooltip = self._container.element(
            f"//div[text()='{self._setting_name}']/ancestor::div[starts-with(@class,'ScormSettings_label')]/div[contains(@class,'Tooltip')]"
        )

    def is_checked(self):
        return self.checkbox.matching(have.attribute("checked"))

    def modify_checkbox(self, checked):
        if self.is_checked() != checked:
            self.checkbox.click()

    def check_tooltip_message(self, message):
        self.tooltip.should(be.visible)
        self.tooltip.hover()
        tooltip_message = self._container.element(f"//div[text()='{message}']")
        tooltip_message.should(be.visible)
