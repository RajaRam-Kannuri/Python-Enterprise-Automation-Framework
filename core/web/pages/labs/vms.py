from selene import browser

from core.web.pages.platform_base_page import PlatformBaseStaticPage


class VmsPage(PlatformBaseStaticPage):
    URL = "labs/sessions#vms"

    def __init__(self):
        super().__init__(self.URL)
        self.title = browser.element('//header/h1[text()="Virtual machines"]')
