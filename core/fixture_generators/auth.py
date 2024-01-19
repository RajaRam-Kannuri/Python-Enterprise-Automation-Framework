from contextlib import contextmanager

from selene import be

from core.web.pages.identity import IdentityLoginPage
from settings import settings


@contextmanager
def login_user(selene_browser, username):
    selene_browser.open(settings.base_url)
    identity_page = IdentityLoginPage()
    identity_page.is_redirected()
    identity_page.login_user(username)
    identity_page.email_input.should(be.hidden)

    yield selene_browser
