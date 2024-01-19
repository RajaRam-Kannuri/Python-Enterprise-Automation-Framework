from core.web.pages.platform_base_page import PlatformBaseStaticPage


class UsersPage(PlatformBaseStaticPage):
    URL = "portal/users"

    def __init__(self):
        super().__init__(self.URL)
