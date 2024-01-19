from urllib.parse import urljoin

from selene import browser, have

from core.web.pages.base_page import StaticUrlPage
from settings import settings
from util.web.assist.allure import report


class IdentityLoginPage(StaticUrlPage):
    def __init__(self):
        super().__init__(urljoin(settings.base_url_identity, "Account/Login"))
        self.email_input = browser.element('input[name="Input.Email"]')
        self.identity_form = browser.element("main[role=main]")
        self.login_button = browser.element("button[value=login]")
        self.password_input = browser.element('input[name="Input.Password"]')
        self.toast_message = browser.element('div[id="toast-hub"]')
        self.validation_error = browser.element("div.validation-summary-errors")

    @report.step
    def is_redirected(self):
        browser.should(have.url_containing("idp"))
        return self

    @report.step
    def login_user(self, user_key: str):
        user = settings.stand_config.platform_users[user_key]

        self.fill_login_form(email=user.email or user.username, password=user.password)

    @report.step
    def fill_login_form(self, email, password):
        self.email_input.type(email)
        self.password_input.type(password)
        self.login_button.click()
