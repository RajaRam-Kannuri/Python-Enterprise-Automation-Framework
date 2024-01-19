import logging

import allure
import pytest
from _pytest.nodes import Item
from _pytest.runner import CallInfo
from assertpy import assertpy

from settings import Environment, settings
from util.assertions.assertpy_extensions import AssertPyExtensions
from util.labels import CustomLabels


@pytest.fixture(scope="session")
def worker_name(request) -> str:
    if hasattr(request.config, "workerinput"):
        worker = request.config.workerinput["workerid"]
    else:
        worker = "master"
    return worker


@pytest.fixture(scope="session", autouse=True)
def extend_assertpy():
    for attr, val in AssertPyExtensions.__dict__.items():
        if callable(val) and not attr.startswith("_"):
            assertpy.add_extension(val)
    AssertPyExtensions._wrap_assertpy_with_allure_step()


@pytest.fixture(scope="session", autouse=True)
def setup_logging(worker_name):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter2 = logging.Formatter("%s:{name}:{levelname}:{message}" % worker_name, style="{")
    logger.handlers[0].setFormatter(formatter2)


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]):
    """
    Automatically mark all tests with product and api/ui marks for filtering
    """
    for item in items:
        item_path = item.path.relative_to(config.rootpath)

        if item_path.parts[0] != "tests":
            continue

        product_marker = getattr(pytest.mark, item_path.parts[1])
        item.add_marker(product_marker)
        item.add_marker(allure.label(CustomLabels.COMPONENT, item_path.parts[1]))

        # Skip tests for avatar on test stands
        if product_marker.name == "avatar" and settings.stand in (Environment.TEST, Environment.CUSTOM_TEST):
            item.add_marker(pytest.mark.skip(reason="Avatar tests are not available in this environment"))

        # Skip non-applicable tests on production
        if settings.stand == Environment.PRODUCTION and (
            not item.get_closest_marker("ui") or not item.get_closest_marker("smokes")
        ):
            item.add_marker(pytest.mark.skip("Skipping non ui smoke tests on production environment"))


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: Item, call: CallInfo):
    """
    Attach snapshots on test failure
    """

    outcome = yield

    result = outcome.get_result()
    if result.when in ("call", "setup") and result.failed:
        if sessions_manager := item.funcargs.get("browser_sessions_manager"):
            for browser_instance in sessions_manager.active_sessions:
                if not browser_instance.config.last_screenshot:
                    browser_instance.save_screenshot()
                allure.attach.file(
                    source=browser_instance.config.last_screenshot,
                    name=f"screenshot for {browser_instance.description}",
                    attachment_type=allure.attachment_type.PNG,
                )
                if not browser_instance.config.last_page_source:
                    browser_instance.save_page_source()
                allure.attach.file(
                    source=browser_instance.config.last_page_source,
                    name=f"page source for {browser_instance.description}",
                    attachment_type=allure.attachment_type.HTML,
                )


def pytest_report_header():
    return [
        "Stand configuration:",
        f"  Base url = {settings.base_url}",
        f"  Base Identity url = {settings.base_url_identity}",
        f"  Base Assessment UI url = {settings.base_url_assessment_ui}",
        f"  Base Assessment API url = {settings.base_url_assessment_api}",
        f"  Base Labs url = {settings.base_url_labs}",
        f"  Base LMS API url = {settings.base_url_lms_api}",
        f"  Base Platform API url = {settings.base_url_platform_api}",
        f"  Base SCORM API url = {settings.base_url_scorm_api}",
    ]
