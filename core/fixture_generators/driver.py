from collections import OrderedDict
from contextlib import contextmanager

import allure_commons
from selene import Browser, Config
from selene import browser as shared_default_browser
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

import settings
from util.web.assist.selene.report.report import wait_with
from util.web.assist.selenium.types import WebDriverOptions
from util.web.assist.webdriver_manager import set_up, supported


class BrowserSessionsManager:
    def __init__(self):
        self._sessions: OrderedDict[Browser] = OrderedDict()

    def add_session(self, browser_session: Browser):
        if browser_session.description in self._sessions.keys():
            raise KeyError(
                f"You are trying to run second browser with the same name! "
                f"adding {browser_session.description};"
                f" already active browsers are: {[str(browser_session) for browser_session in self._sessions.keys()]}"
            )
        self._sessions[browser_session.description] = browser_session  # noqa: the attribute is from monkeypatching

    def finish_session(self, browser_session: Browser):
        for name, session in self._sessions.items():
            if session == browser_session:
                session.quit()
                del self._sessions[name]
                break

    @property
    def active_sessions(self) -> tuple[Browser]:
        return tuple(self._sessions.values())


@contextmanager
def setup_default_browser(settings_instance: settings.Settings, sessions_manager: BrowserSessionsManager) -> Browser:
    shared_default_browser.config.base_url = settings_instance.base_url
    shared_default_browser.config.timeout = settings_instance.default_ui_timeout
    shared_default_browser.config.save_page_source_on_failure = settings_instance.save_page_source_on_failure
    shared_default_browser.config._wait_decorator = wait_with(context=allure_commons._allure.StepContext)
    shared_default_browser.config.driver = _driver_from(settings_instance)

    shared_default_browser.as_(settings_instance.default_browser_name)  # noqa: the attribute is from monkeypatching

    sessions_manager.add_session(shared_default_browser)

    yield shared_default_browser

    shared_default_browser.config.hold_driver_at_exit = settings_instance.hold_driver_at_exit
    if not settings_instance.hold_driver_at_exit:
        sessions_manager.finish_session(shared_default_browser)


@contextmanager
def setup_secondary_browser(
    settings_instance: settings.Settings, sessions_manager: BrowserSessionsManager, browser_name: str
) -> Browser:
    # We need this check because of the way element locator names are compiled.
    # See DefaultTranslations for more information.
    if browser_name.endswith(settings_instance.default_browser_name):
        raise ValueError(
            f"Browser name {browser_name} should not end with {settings_instance.default_browser_name}. "
            f"Please, use another name."
        )

    config = Config(
        base_url=settings_instance.base_url,
        timeout=settings_instance.default_ui_timeout,
        save_page_source_on_failure=settings_instance.save_page_source_on_failure,
        _wait_decorator=wait_with(context=allure_commons._allure.StepContext),
    )
    browser_instance = Browser(config)
    browser_instance.config.driver = _driver_from(settings_instance)

    browser_instance.as_(browser_name)  # noqa: the attribute is from monkeypatching
    sessions_manager.add_session(browser_instance)

    yield browser_instance

    browser_instance.config.hold_driver_at_exit = settings_instance.hold_driver_at_exit
    if not settings_instance.hold_driver_at_exit:
        sessions_manager.finish_session(browser_instance)


def _driver_from(settings_instance: settings.Settings) -> WebDriver:
    driver_options = _driver_options_from(settings_instance)
    if settings_instance.chrome_path:
        driver_options.binary_location = settings_instance.chrome_path

    driver = (
        set_up.local(
            settings_instance.browser_type,
            driver_options,
        )
        if not settings_instance.remote_url
        else webdriver.Remote(
            command_executor=settings_instance.remote_url,
            options=driver_options,
        )
    )

    if settings_instance.maximize_window:
        driver.maximize_window()
    else:
        driver.set_window_size(
            width=settings_instance.window_width,
            height=settings_instance.window_height,
        )

    return driver


def _driver_options_from(settings_instance: settings.Settings) -> WebDriverOptions:
    options = None

    if settings_instance.browser_type in [supported.chrome, supported.chromium]:
        options = webdriver.ChromeOptions()
        if settings_instance.headless:
            options.add_argument("--headless=new")
        options.add_argument(f"--window-size={settings_instance.window_width},{settings_instance.window_height}")
        if settings_instance.log_chrome_network:
            options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        if settings_instance.disable_audio:
            options.add_argument("--mute-audio")

    if settings_instance.browser_type == supported.firefox:
        options = webdriver.FirefoxOptions()
        options.headless = settings_instance.headless

    if settings_instance.browser_type == supported.ie:
        options = webdriver.IeOptions()

    from util.web.assist.selenium.types import EdgeOptions

    if settings_instance.browser_type == supported.edge:
        options = EdgeOptions()

    if settings_instance.remote_url:
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(f"--enable-video={str(settings_instance.remote_enable_video).lower()}")
        options.add_argument(f"--enable-vnc={str(settings_instance.remote_enable_vnc).lower()}")
        options.add_argument(f"--enable-log={str(settings_instance.remote_enable_log).lower()}")
        if settings_instance.remote_version:
            options.add_argument(f"--version={settings_instance.remote_version}")
        if settings_instance.remote_platform:
            options.add_argument(f"--platform={settings_instance.remote_platform}")

    if settings_instance.browser_type in [supported.chrome, supported.chromium]:
        options.add_argument("--use-fake-ui-for-media-stream")
        options.add_argument("--use-fake-device-for-media-stream")
    elif settings_instance.browser_type == supported.edge:
        options.set_capability("useFakeDeviceForMediaStream", True)
        options.set_capability("useFakeUIForMediaStream", True)
    elif settings_instance.browser_type == supported.firefox:
        profile = webdriver.FirefoxProfile()
        profile.set_preference("media.navigator.permission.disabled", False)
        profile.set_preference("media.navigator.streams.fake", True)
        options.profile = profile

    return options
