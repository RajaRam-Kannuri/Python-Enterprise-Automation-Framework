from datetime import datetime, timedelta

import pytest
from requests import Session
from selene import Browser, be, have, query

from core.api.platform.user import UsersApi
from core.models.platform.platform_user import PlatformUser
from core.web.pages.classroom.classrooms import ClassRoomPage
from core.web.pages.classroom.create_class import CreatePage
from core.web.pages.classroom.create_session import CreateSessionPage
from core.web.pages.classroom.instant_session import InstantSessionPage
from core.web.pages.classroom.online_session import OnlineSessionPage
from core.web.pages.lms.content_library_pages.content_library import ContentLibraryPage
from core.web.pages.platform.users_page import UsersPage
from util.random import random_string, random_text


@pytest.fixture(scope="module")
def tenant_user(all_roles_session: Session) -> PlatformUser:
    users_api = UsersApi(all_roles_session)
    return users_api.get_current_user()


@pytest.fixture
def users_page(logged_in_user: Browser) -> UsersPage:
    page = UsersPage().open().should_be_opened()
    return page


@pytest.fixture
def session_page(logged_in_user):
    session_page = OnlineSessionPage().open().should_be_opened()
    return session_page


@pytest.fixture
def content_page(logged_in_user):
    content_page = ContentLibraryPage().open().should_be_opened()
    return content_page


@pytest.fixture
def class_page(logged_in_user):
    class_page = ClassRoomPage().open().should_be_opened()
    return class_page


@pytest.fixture()
def classroom(logged_in_user):
    create_class_page = CreatePage().open().should_be_opened()
    class_name = random_string(min_length=20, prefix="Demo Class")
    create_class_page.name_input.type(class_name)
    create_class_page.description_input.type(
        "This is a small demo virtual lab that will give you the idea how it works for the learner."
    )
    create_class_page.save_button.click()
    ClassRoomPage().get_class_title.should(have.text(class_name))
    return class_name


@pytest.fixture()
def session_creation_page(logged_in_user):
    create_session_page = CreateSessionPage().open().should_be_opened()
    create_session_page.attach_current_tab()
    session_title = random_text(10)
    create_session_page.name_form.fill_with_text(session_title)
    create_session_page.description_form.fill_with_text(random_text(30))
    create_session_page.set_session_time(
        start=create_session_page.round_time(datetime.now()),
        end=create_session_page.round_time(datetime.now() + timedelta(minutes=30)),
    )
    create_session_page.create_session_button.click()
    create_session_page.page_title.should(have.text(session_title))
    return create_session_page


@pytest.fixture()
def host_session(session_creation_page):
    guest_session_link = session_creation_page.guest_session_link.get(query.value)
    session_name = session_creation_page.name_form.input.get(query.value)
    session_creation_page.update_session_button.click()
    session_page = OnlineSessionPage().open().should_be_opened()
    session_page.session_table.should_be_loaded()
    session_page.session_search_input.type(session_name)
    session_page.session_table.get_row_by_cell_value(
        column_name="Session name", value=session_name
    ).start_session_button.click()
    session = InstantSessionPage()
    session.mic_button.should(be.clickable).click()
    session.disable_video()
    session.start_session_button.click()
    session.participant_video.should(be.visible)

    yield guest_session_link

    session.exit_option_button.click()
    session.end_session_modal.end_for_all_button.click()


@pytest.fixture()
def manage_session(session_page):
    session_page.create_session_dropdown.select_item_by_text("Start instant session")
    instant_session = InstantSessionPage()
    instant_session.disable_video()
    instant_session.start_session_button.should(have.text("Start the session")).click()
    start_time = datetime.now()
    instant_session.participant_video.should(be.visible)
    instant_session.exit_option_button.click()
    instant_session.end_session_modal.end_for_all_button.click()
    end_time = datetime.now()
    instant_session.confirmation_text.should(have.text("Session is ended"))
    session_page.open().should_be_opened()
    return start_time, end_time, session_page


@pytest.fixture()
def instant_session(session_page):
    session_page.create_session_dropdown.select_item_by_text("Start instant session")
    instant_session = InstantSessionPage()
    instant_session.participant_name_input.should(be.visible)
    instant_session.disable_video()
    instant_session.mic_button.click()
    instant_session.start_session_button.click()
    yield instant_session


@pytest.fixture()
def guest_link(instant_session):
    instant_session.more_button.click()
    guest_link = instant_session.more_options_modal.guest_link.get(query.value)
    instant_session.more_options_modal.close()
    return guest_link


@pytest.fixture()
def guest_session(guest_link, second_browser):
    second_browser.open(guest_link)
    guest_session = InstantSessionPage(second_browser)
    guest_session.participant_name_input.set_value("Guest participant")
    guest_session.disable_video()
    guest_session.mic_button.click()
    guest_session.start_session_button.click()
    guest_session.participant_video.should(be.visible)
    return guest_session


@pytest.fixture()
def setup_moderator_role(instant_session, guest_session):
    instant_session.participant_list_button.click()
    instant_session.participant_list_items.should(have.size(2))
    instant_session.presenter.role_menu.select_menu_and_submenu_by_text("Roles", "Make a Moderator")
    instant_session.side_menu_close_button.click()
    yield instant_session, guest_session


@pytest.fixture()
def setup_presenter_role(instant_session, guest_session):
    instant_session.participant_list_button.click()
    instant_session.participant_list_items.should(have.size(2))
    instant_session.presenter.role_menu.select_menu_and_submenu_by_text("Roles", "Make a Presenter")
    instant_session.side_menu_close_button.click()
    yield instant_session, guest_session


@pytest.fixture()
def second_guest(guest_link, third_browser):
    third_browser.open(guest_link)
    session = InstantSessionPage(third_browser)
    session.participant_name_input.set_value("Third participant")
    session.disable_video()
    session.mic_button.click()
    session.start_session_button.click()
    session.participant_video.should(be.visible)
    return session
