from core.web.pages.platform_base_page import PlatformBaseStaticPage


class TenantsPage(PlatformBaseStaticPage):
    URL = "portal/tenants"

    def __init__(self):
        super().__init__(self.URL)
