from typing import Union

import selenium
from selenium.webdriver.edge.options import Options as EdgeOptions

WebDriverOptions = Union[
    selenium.webdriver.ChromeOptions,
    selenium.webdriver.FirefoxOptions,
    selenium.webdriver.IeOptions,
    EdgeOptions,
]
