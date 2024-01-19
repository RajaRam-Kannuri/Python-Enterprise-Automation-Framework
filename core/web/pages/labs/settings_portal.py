from selene import browser

from core.web.pages.platform_base_page import PlatformBaseStaticPage


class SettingsPage(PlatformBaseStaticPage):
    URL = "portal/settings"

    def __init__(self):
        super().__init__(self.URL)
        self.labs_group_container = browser.element(
            './/*[contains(@class, "SettingsPageGroup_group") and ' './/h4[text()="Labs"]]'
        )
        self.button_environments = self.labs_group_container.element('.//button[text()="Environments"]')
        self.button_images = self.labs_group_container.element('.//button[text()="Images"]')
