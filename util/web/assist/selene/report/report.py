"""
The code in this file is basically the code from selene.support, slightly modified to support custom chained names and
their hidden locators.
"""
import re
from functools import reduce
from typing import Any, ContextManager, Dict, Iterable, Protocol, Tuple

from selene import Collection, Element
from selene.core.entity import Browser, WaitingEntity
from selene.core.locator import Locator
from selenium.webdriver import Keys

from settings import settings
from util.web.assist.allure import report
from util.web.assist.python import monkey


class _ContextManagerFactory(Protocol):
    def __call__(self, *, title: str, params: Dict[str, Any], **kwargs) -> ContextManager:
        ...


class DefaultTranslations:
    remove_verbosity = (
        (f"{settings.default_browser_name}.element", "element"),
        (f"{settings.default_browser_name}.all", "all"),
        ("'css selector', ", ""),
        ("((", "("),
        ("))", ")"),
    )
    identify_assertions = (
        (": has ", ": have "),
        (": have ", ": should have "),
        (": is ", ": should be "),
        (" and is ", " and be "),
        (" and has ", " and have "),
    )
    key_codes_to_names = [
        (f"({repr(value)},)", key) for key, value in Keys.__dict__.items() if not key.startswith("__")
    ]


def wait_with(
    *,
    context: _ContextManagerFactory,
    translations: Iterable[Tuple[str, str]] = (
        *DefaultTranslations.remove_verbosity,
        *DefaultTranslations.identify_assertions,
        *DefaultTranslations.key_codes_to_names,
    ),
):
    """
    :return:
        Decorator factory to pass to Selene's config._wait_decorator
        for logging commands with waiting built in
    :param context:
        Allure-like ContextManager factory
        (i.e. a type/class or function to return python context manager),
        that builds a context manager based on title string and params dict
    :param translations:
        Iterable of translations as (from, to) substitution pairs
        to apply to final title string to log
    """

    def decorator_factory(wait):
        def decorator(for_):
            def decorated(fn):
                title = f"{wait.entity}: {fn}"

                # full_description is from monkeypathing of selene's element
                if isinstance(wait.entity, Element) or isinstance(wait.entity, Collection):
                    title = f"{wait.entity.full_description}: {fn}"

                def translate(initial: str, item: Tuple[str, str]):
                    old, new = item
                    return initial.replace(old, new)

                translated_title = reduce(
                    translate,
                    translations,
                    title,
                )
                params = {}
                if isinstance(wait.entity, Element) or isinstance(wait.entity, Collection):
                    translated_locator = reduce(
                        translate,
                        translations,
                        str(wait.entity),
                    )
                    params = {"locator": translated_locator}
                with context(title=translated_title, params=params):
                    return for_(fn)

            return decorated

        return decorator

    return decorator_factory


def add_reporting_to_selene_steps():
    original_open = Browser.open

    @monkey.patch_method_in(Browser)
    def open(self, relative_or_absolute_url: str):
        return report.step(original_open)(self, relative_or_absolute_url)

    @monkey.patch_method_in(Browser)
    def __str__(self):
        return self.description

    # we need the last part of the locator for use as a name in case a description wasn't provided
    @monkey.patch_method_in(Locator)
    def last_locator(self):
        result = re.search(r"""(element|all)\(\('[^()]*', '[^']*'\)\)$""", self._description)
        return result.group()

    WaitingEntity.description = ""
    WaitingEntity.previous_name_chain_element = None
    WaitingEntity.full_description = ""

    @monkey.patch_method_in(WaitingEntity)
    def as_(self, name: str):
        self.description = name
        return self

    @property
    def full_description(self):
        if self.description:
            result = self.get_full_path()
        else:
            result = str(self._locator)
        return result

    Collection.full_description = full_description
    Element.full_description = full_description

    @monkey.patch_method_in(WaitingEntity)
    def get_full_path(self):
        result = ".".join(self.resolve_name())
        return result

    @monkey.patch_method_in(WaitingEntity)
    def resolve_name(self) -> list:
        if self.previous_name_chain_element:
            name = self.previous_name_chain_element.resolve_name()
        else:
            name = []
        name.append(str(self.description or str(self.last_locator())))
        return name
