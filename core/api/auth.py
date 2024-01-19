import os
from types import NoneType
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from requests import Response, Session

from core.models.idp import LoginForm
from core.models.user import LabsUser, User
from settings import Environment, settings
from util.helpers import extract_value_from_html

client_data = {
    "client_id": os.environ.get("PROD_LABS_CLIENT_ID") if settings.stand == Environment.PRODUCTION else "insomnia",
    "client_secret": os.environ.get("PROD_LABS_SECRET") if settings.stand == Environment.PRODUCTION else "insomnia",
    "scope": "comm-hub-admin impersonate openid platform profile user user-password",
}


def _auth_request(session: Session, data: dict):
    response = session.post(settings.idp_token_url, data=data)
    response.raise_for_status()
    token = response.json()["access_token"]
    session.headers.update({"Authorization": f"Bearer {token}"})


def authorize_app(session: Session):
    data = {
        **client_data,
        "grant_type": "client_credentials",
    }
    _auth_request(session, data)


def authorize_platform_user(session: Session, user: User):
    data = {
        **user.dict(include={"username", "password"}),
        **client_data,
        "grant_type": "password",
    }
    _auth_request(session, data)


def authorize_labs_user(session: Session, user: LabsUser):
    response = session.post(url=f"{settings.base_url_labs}/api/auth/login", json={**user.dict(), **client_data})
    response.raise_for_status()
    session.headers.update({"Authorization": f"Token {response.json().get('token')}"})


def authorize_user_with_cookies(session: Session, user: User):
    emulate_login(session, user)


def do_nothing(*args, **kwargs):
    """For non-authorized cases"""


authorization_ways = {NoneType: do_nothing, User: authorize_platform_user, LabsUser: authorize_labs_user}


def emulate_login(
    session: Session,
    user: User,
    login_form_url: str = urljoin(settings.base_url, "oidc/login"),
    login_form_data: dict | None = None,
) -> Response:
    """
    Emulate oidc login flow with specified user.
    Calls by default to oidc/login endpoint to generate html login form.
    Uses form data to call authorization endpoint to get authorization cookies.
    login_form_url: - url to generate html login form. can be overridden by lti to link resources
    login_form_data: - used with lti mode to generate proper login form.

    Returns response to authorization endpoint:
     - With regular login it is redirected to base url. Authorization cookies are applied to the session object.
     - With lti login it contains lti data and tokens for further use in lti
    """
    login_form_response = session.post(login_form_url, data=login_form_data if login_form_data else None)
    if not login_form_response.ok or not login_form_response.text:
        raise RuntimeError("Failed to get login html form")

    form = BeautifulSoup(login_form_response.text, "html.parser").find("form", id="account")
    if form:
        # Login form exists in response. Authorize the user
        login_data = LoginForm(
            return_url=extract_value_from_html(form, "Input.ReturnUrl"),
            email=user.username,
            password=user.password,
            remember_login=extract_value_from_html(form, "Input.RememberLogin"),
            button=extract_value_from_html(form, "button"),
            request_verification_token=extract_value_from_html(form, "__RequestVerificationToken"),
        )
        login_response = session.post(
            settings.idp_login_url, data=login_data.lms_dict(), params={"ReturnUrl": login_data.return_url}
        )
    else:
        # Login form does not exist in response. Assume that user is already authorized
        login_response = login_form_response

    if not login_response.ok:
        raise ValueError("Failed to perform login.")

    return login_response
