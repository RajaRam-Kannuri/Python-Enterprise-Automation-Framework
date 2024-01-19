from selene import Browser
from selene.common import predicate
from selene.core.condition import Condition
from selene.core.conditions import BrowserCondition


def browser_has_url_path(
    expected: str,
    describing_matched_to="has url path",
    compared_by_predicate_to=predicate.equals,
) -> Condition[Browser]:
    def url_path(browser: Browser) -> str:
        return browser.driver.current_url.split("?", maxsplit=1)[0]

    return BrowserCondition.raise_if_not_actual(
        f"{describing_matched_to} '{expected}'",
        url_path,
        compared_by_predicate_to(expected),
    )
