import gzip
import json
import logging
import os

import allure
import pytest
import requests
import waiting
from requests import HTTPError
from selene import Browser, browser
from waiting import TimeoutExpired

from core.api.base_refactored.api_wrapper import ApiWrapper
from core.api.session_manager import SessionManager
from core.fixture_generators.auth import login_user
from core.fixture_generators.driver import BrowserSessionsManager, setup_default_browser, setup_secondary_browser
from settings import settings
from util.web.assist.selene.report.report import add_reporting_to_selene_steps


@pytest.fixture(scope="module")
def logged_in_user(default_browser) -> Browser:
    with login_user(default_browser, "all_roles") as selene_browser:
        yield selene_browser


@pytest.fixture(scope="session")
def session_manager() -> SessionManager:
    yield SessionManager()


@pytest.fixture(scope="session")
def browser_sessions_manager() -> BrowserSessionsManager:
    """
    The fixture is used to track and manage all active browser sessions.
    """
    manager = BrowserSessionsManager()
    yield manager


@pytest.fixture(scope="session")
def admin_session(session_manager) -> requests.Session:
    yield session_manager.get_session("admin")


@pytest.fixture(scope="session")
def all_roles_session(session_manager) -> requests.Session:
    yield session_manager.get_session("all_roles")


@pytest.fixture(scope="session")
def author_session(session_manager) -> requests.Session:
    yield session_manager.get_session("author")


@pytest.fixture(scope="session")
def instructor_session(session_manager) -> requests.Session:
    yield session_manager.get_session("instructor")


@pytest.fixture(scope="session")
def learner_session(session_manager) -> requests.Session:
    yield session_manager.get_session("learner")


@pytest.fixture(scope="session")
def parameterizable_http_session(request, session_manager) -> requests.Session:
    user_key = getattr(request, "param", "all_roles")
    yield session_manager.get_session(user_key=user_key)


@pytest.fixture
def create_session(session_manager):
    def generate(user_key):
        return session_manager.get_session(user_key)

    yield generate


class TeardownListForApiObjects(list):
    def append(self, teardown_object: ApiWrapper):
        if not isinstance(teardown_object, ApiWrapper):
            raise AttributeError
        logging.info(f"adding an {teardown_object} to the deletion set")
        super().append(teardown_object)


@pytest.fixture
def teardown_bucket():
    bucket = TeardownListForApiObjects()
    yield bucket

    for element in bucket:
        element.teardown()


@pytest.fixture(scope="session")
def global_teardown_bucket():
    bucket: TeardownListForApiObjects[ApiWrapper] = TeardownListForApiObjects()
    yield bucket

    logging.info("deleting objects in a global teardown list...")
    max_timeout = max((element.teardown_timeout for element in bucket), default=0)

    def try_to_delete_all_items():
        """The function tries to delete all the objects"""
        remaining_elements = [el for el in bucket if not el.is_finalized]
        logging.info(f"trying to finalize {len(remaining_elements)} objects")
        logging.debug(f"the list of objects to finalize: {remaining_elements}")
        for element in remaining_elements:
            try:
                element.teardown()
            except HTTPError as error:
                if error.response.status_code == 404:
                    element.is_exist_on_backend = False
                else:
                    raise error

    try:
        waiting.wait(
            lambda: all(el.is_finalized for el in bucket),
            on_poll=try_to_delete_all_items,
            sleep_seconds=5,
            timeout_seconds=max_timeout,
            waiting_for="until all items will be finalized",
            expected_exceptions=(HTTPError, KeyError),
        )
    except TimeoutExpired:
        not_deleted_items = [el for el in bucket if not el.is_finalized]
        raise TimeoutError(f"{len(not_deleted_items)} items were not deleted: {not_deleted_items}")


@allure.title("browser invoked once per session")
@pytest.fixture(scope="module")
def default_browser(browser_sessions_manager):
    with setup_default_browser(settings, browser_sessions_manager) as selene_browser:
        yield selene_browser


@allure.title("second browser instance")
@pytest.fixture()
def second_browser(browser_sessions_manager):
    """
    A second browser instance may be used to handle some complex multi-user test cases.
    However, in most cases, it's better to use api-calls or a second browser tab.

    Returns: the second Browser instance

    """

    with setup_secondary_browser(
        settings, sessions_manager=browser_sessions_manager, browser_name="second_browser"
    ) as selene_browser:
        yield selene_browser


@allure.title("third browser instance")
@pytest.fixture()
def third_browser(browser_sessions_manager):
    with setup_secondary_browser(
        settings, sessions_manager=browser_sessions_manager, browser_name="third_browser"
    ) as selene_browser:
        yield selene_browser


@pytest.fixture(scope="function")
def save_chrome_logs(default_browser, request, worker_name):
    """
    To save logs, set settings.log_chrome_network to True.

    This fixture supports only one (default) browser instance.
    """
    yield
    if request.node.get_closest_marker("ui") and settings.log_chrome_network:
        test_name = os.environ.get("PYTEST_CURRENT_TEST").split(":")[-1].split(" ")[0]
        path = request.config.rootpath / "chrome_logs"
        os.makedirs(path, exist_ok=True)

        # pay attention: get_log() removes the received logs in a driver storage.
        # Thus, you can not get the same logs twice from a driver.
        logs = browser.driver.get_log("performance")

        with gzip.open(path / f"{worker_name}.{browser.driver.session_id}.gz", "at", compresslevel=4) as archived_file:
            for entry in logs:
                log = json.loads(entry["message"])["message"]
                if "Network.response" in log["method"] or "Network.request" in log["method"]:
                    log["test_name"] = test_name
                    log["timestamp"] = entry["timestamp"]
                    json.dump(log, archived_file)
                    archived_file.write("\n")


@pytest.fixture(autouse=True)
def check_tabs_amount(request):
    yield
    if browser_session_manager := request.node.funcargs.get("browser_sessions_manager"):
        for browser_instance in browser_session_manager.active_sessions:
            with allure.step(f"checking that there are no extra tabs left in a browser {browser_instance}"):
                message = (
                    f"actual amount of tabs for {browser_instance} = {len(browser_instance.driver.window_handles)}"
                )
                logging.debug(message)
                assert len(browser_instance.driver.window_handles) == 1, message


def pytest_sessionstart():
    add_reporting_to_selene_steps()
