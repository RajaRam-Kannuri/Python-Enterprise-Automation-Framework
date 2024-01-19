import urllib.parse
from enum import StrEnum
from functools import cached_property
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

import requests
from pydantic import BaseSettings, root_validator

from test_data.stand_config import (
    CUSTOM_DOMAIN_DEV_CONFIG,
    CUSTOM_DOMAIN_STAGE_CONFIG,
    CUSTOM_DOMAIN_TEST_CONFIG,
    DEV_CONFIG,
    PROD_CONFIG,
    STAGE_CONFIG,
    TEST_CONFIG,
    StandConfig,
)
from util.url import add_domain_prefix
from util.web.assist.webdriver_manager import supported

PROJECT_ROOT = Path(__file__).parent.absolute()


class Environment(StrEnum):
    DEVELOPMENT = "dev"
    TEST = "test"
    STAGING = "stage"
    PRODUCTION = "prod"
    CUSTOM_DEVELOPMENT = "custom_dev"
    CUSTOM_TEST = "custom_test"
    CUSTOM_STAGING = "custom_stage"


ENVIRONMENT_BASE_URLS = {
    Environment.DEVELOPMENT: "https://dev.alemira.cloud/",
    Environment.TEST: "https://test.alemira.com/",
    Environment.STAGING: "https://stage.alemira.cloud/",
    Environment.PRODUCTION: "https://constructor.app/",
    Environment.CUSTOM_DEVELOPMENT: "https://cldev-dummy-tenant.alemira.dev/",
    Environment.CUSTOM_TEST: "https://dummy-tenant-for-test.alemira.dev/",
    Environment.CUSTOM_STAGING: "https://clstage-dummy-tenant.alemira.dev/",
}

ENVIRONMENT_IDENTITY_BASE_URLS = {Environment.PRODUCTION: "https://idp.constructor.app/"}

ENVIRONMENT_STAND_CONFIGS = {
    Environment.PRODUCTION: PROD_CONFIG,
    Environment.DEVELOPMENT: DEV_CONFIG,
    Environment.TEST: TEST_CONFIG,
    Environment.STAGING: STAGE_CONFIG,
    Environment.CUSTOM_DEVELOPMENT: CUSTOM_DOMAIN_DEV_CONFIG,
    Environment.CUSTOM_TEST: CUSTOM_DOMAIN_TEST_CONFIG,
    Environment.CUSTOM_STAGING: CUSTOM_DOMAIN_STAGE_CONFIG,
}


class Settings(BaseSettings):
    # common settings section:
    debug: bool = False
    stand: Environment = Environment.STAGING
    assertpy_argument_length_limit: int = 50

    # urls settings section:
    base_url: str = ""
    base_url_identity: str = ""
    base_url_assessment_ui: str = ""
    base_url_assessment_api: str = ""
    base_url_labs: str = ""
    base_url_content_libraries: str = ""
    base_url_lms_api: str = ""
    base_url_scorm_api: str = ""
    base_url_platform_api: str = ""
    base_url_scorm: str = ""
    base_url_avatar: str = ""

    # UI settings section:
    log_chrome_network: bool = False
    default_ui_timeout: float = 30.0
    disable_audio: bool = False
    browser_type: supported.BrowserName = "chrome"
    headless: bool = True
    window_width: int = 1920
    window_height: int = 1080
    maximize_window: bool = False
    use_remote: bool = True
    grid_username: str = ""
    grid_password: str = ""
    remote_link_template: str = "https://{grid_username}:{grid_password}@selenium-grid.stage.constr.dev"
    remote_version: str | None = None
    remote_platform: str | None = None
    remote_enable_vnc: bool = True
    remote_enable_video: bool = False
    remote_enable_log: bool = True
    hold_driver_at_exit: bool = False
    save_page_source_on_failure: bool = True
    chromedriver_path: str | None = None
    chrome_path: str | None = None
    default_browser_name: str = "default_browser"
    recheck_timeout: float = 3.0

    # API settings section:
    default_api_timeout: float = 30.0

    # labs settings section:
    code_server_starting_timeout: float = 80.0
    coding_lab_general_timeout: float = 60.0
    image_preparation_timeout = 300

    # lms settings section:
    default_command_timeout: float = 10
    default_command_sleep: float = 0.5

    @root_validator
    def fill_default_urls(cls, values: dict[str, Any]) -> dict[str, Any]:
        stand = values.get("stand")

        if values.get("base_url"):
            base_url = values["base_url"]
        else:
            base_url = ENVIRONMENT_BASE_URLS.get(stand)
            values["base_url"] = base_url

        if not base_url:
            raise ValueError("Base url missing. Set BASE_URL environment variable.")

        if not values.get("base_url_identity"):
            values["base_url_identity"] = ENVIRONMENT_IDENTITY_BASE_URLS.get(stand) or urljoin(base_url, "idp/")

        if not values.get("base_url_assessment_ui"):
            values["base_url_assessment_ui"] = urljoin(base_url, "assessment/")

        if not values.get("base_url_assessment_api"):
            values["base_url_assessment_api"] = urljoin(base_url, "api/assessment/")

        if not values.get("base_url_labs"):
            values["base_url_labs"] = urljoin(base_url, "labs/")

        if not values.get("base_url_lms_api"):
            values["base_url_lms_api"] = urljoin(base_url, "api/lms/v1/")

        if not values.get("base_url_scorm_api"):
            values["base_url_scorm_api"] = urljoin(base_url, "api/scorm/v1/")

        if not values.get("base_url_platform_api"):
            values["base_url_platform_api"] = urljoin(base_url, "api/platform/v1/")

        if not values.get("base_url_scorm"):
            values["base_url_scorm"] = add_domain_prefix(base_url, "scorm")

        if not values.get("base_url_avatar"):
            values["base_url_avatar"] = urljoin(base_url, "avatar/")

        return values

    @cached_property
    def _idp_config(self) -> dict[str, Any]:
        url = urllib.parse.urljoin(self.base_url_identity, ".well-known/openid-configuration")
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    @property
    def idp_token_url(self) -> str:
        return self._idp_config["token_endpoint"]

    @property
    def idp_login_url(self) -> str:
        return f"{self.base_url_identity}Account/Login"

    @property
    def idp_logout_url(self) -> str:
        return f"{self.base_url_identity}Account/Logout"

    @property
    def remote_url(self) -> str:
        if self.use_remote:
            url = self.remote_link_template.format(grid_username=self.grid_username, grid_password=self.grid_password)
        else:
            url = ""
        return url

    @property
    def stand_config(self) -> StandConfig:
        return ENVIRONMENT_STAND_CONFIGS[self.stand]

    class Config:
        env_file = [PROJECT_ROOT / ".env", PROJECT_ROOT / ".env.local"]
        env_prefix = ""
        case_sensitive = False


settings = Settings()
