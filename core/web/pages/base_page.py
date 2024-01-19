import logging
from typing import Self
from urllib.parse import urljoin

import allure
from selene import Browser, browser
from selenium.common import NoSuchWindowException
from urllib3.exceptions import MaxRetryError, NewConnectionError

from settings import settings
from util.web.assist.allure import report
from util.web.assist.allure.chainable_naming import ChainableNamingElement
from util.web.assist.selene.extended import have


class BasePage(ChainableNamingElement):
    def __str__(self):
        if self.browser.description == settings.default_browser_name:  # noqa: the attribute is from monkeypatching
            return self.__class__.__name__
        return f"{self.browser.description}:{self.__class__.__name__}"  # noqa: the attribute is from monkeypatching

    def __init__(self, browser_instance: Browser = browser):
        super().__init__()
        self.attached_tab_id = None
        self.browser = browser_instance

    def attach_browser_tab(self, tab_index: int) -> Self:
        """Attach to a page the related tab to switch or close later. Attaching does not mean switching.

        Args:
            tab_index: tab index starting from #1

        """
        self.browser.wait_until(have.tabs_number(tab_index))
        self.attached_tab_id = self.browser.driver.window_handles[tab_index - 1]
        return self

    def attach_current_tab(self) -> Self:
        """Attach to a page the opened tab to switch or close later."""

        self.attached_tab_id = self.browser.driver.current_window_handle
        return self

    @report.step
    def make_related_tab_active(self) -> Self:
        with allure.step(f'activating a browser tab "{self.attached_tab_id}"'):
            self.browser.switch_to_tab(self.attached_tab_id)
            return self

    @report.step
    def close_related_tab(self):
        """
        The method closes related to a page tab and activates the first one. The method useful for finalization in
        tests.
        If used in a test with more than 2 tabs, use make_related_tab_active() after the call:
        page3.close_related_tab()
        page2.make_related_tab_active()
        page2.do_something()

        """
        try:
            tabs_amount_before = len(self.browser.driver.window_handles)
            self.browser.switch_to_tab(self.attached_tab_id)
            self.browser.driver.close()
            self.browser.should(have.tabs_number(tabs_amount_before - 1))
            self.browser.switch_to_tab(0)
        except (ConnectionRefusedError, NewConnectionError, MaxRetryError):
            logging.info("An attempt to close the tab was unsuccessful. Does the browser still exist?")
        except NoSuchWindowException:
            logging.info("An attempt to close the tab was unsuccessful. The window was closed previously")
            self.browser.switch_to_tab(0)

    @report.step
    def refresh(self) -> Self:
        self.browser.driver.refresh()
        return self


class StaticUrlPage(BasePage):
    def __init__(self, url: str):
        super().__init__()
        self.url = url

    @report.step
    def open(self) -> Self:
        browser.open(self.url)
        self.attach_current_tab()
        return self

    @report.step
    def should_be_opened(self) -> Self:
        url = urljoin(browser.config.base_url, self.url)
        browser.should(have.url_path_matching(url).or_(have.url_path_matching(url + "/")))
        return self

    @report.step
    def open_in_a_new_tab(self) -> Self:
        browser.execute_script("window.open('');")
        browser.switch_to_next_tab()
        self.open()
        return self


class DynamicUrlPage(BasePage):
    def __init__(self, url_template: str, browser_instance: Browser = browser):
        super().__init__(browser_instance=browser_instance)
        self.url_template = url_template
