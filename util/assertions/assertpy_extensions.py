from functools import wraps
from typing import List

import allure
from assertpy.assertpy import AssertionBuilder
from pydantic import BaseModel

from settings import settings


class AssertPyExtensions:
    @staticmethod
    def is_all_items_has_field_equal_to(assertpy_self, field_name, field_value):
        with allure.step(f"Asserting that all items in list has '{field_value}' as {field_name}"):
            owner_ids = [getattr(assessment, field_name) for assessment in assertpy_self.val]
            if not all(owner_id == field_value for owner_id in owner_ids):
                assertpy_self.error(f"not all {field_name} equal to {field_value}")
            return assertpy_self

    @staticmethod
    def is_all_items_has_field_satisfying_condition(assertpy_self, field_name, condition, condition_description):
        with allure.step(
            f"Asserting that all items in list has {field_name} "
            f"satisfying following condition '{condition_description}'"
        ):
            field_values = [getattr(assessment, field_name) for assessment in assertpy_self.val]
            if not all(condition(field_value) for field_value in field_values):
                assertpy_self.error(
                    f"In {assertpy_self.val} not all {field_name} "
                    f"satisfy following condition: '{condition_description}'"
                )
            return assertpy_self

    @staticmethod
    def is_all_items_has_one_of_the_fields_satisfying_condition(
        assertpy_self, field_names, condition, condition_description
    ):
        with allure.step(
            f"Asserting that all items in list has one of the field {field_names} "
            f"satisfying following condition '{condition_description}'"
        ):
            for item in assertpy_self.val:
                field_values = [getattr(item, field_name) for field_name in field_names]
                if not any(condition(field_value) for field_value in field_values):
                    assertpy_self.error(
                        f"In {assertpy_self.val} not all items has one of the field {field_names} "
                        f"satisfy following condition: '{condition_description}'"
                    )
            return assertpy_self

    @staticmethod
    def is_all_model_fields_equal(assertpy_self, expected_model, excluded_fields: [str] = None):
        if not isinstance(assertpy_self.val, BaseModel):
            raise ValueError("compared items should inherit pydantic BaseModel")
        if type(assertpy_self.val) != type(expected_model):
            raise ValueError("compared models should have same type")
        with allure.step(f"Asserting that models has all fields equal excluding '{excluded_fields or ''}' "):
            excluded_fields = excluded_fields or []
            fields_to_compare = [
                attr for attr in assertpy_self.val.schema()["properties"].keys() if attr not in excluded_fields
            ]
            if not all(
                [getattr(assertpy_self.val, attr) == getattr(expected_model, attr) for attr in fields_to_compare]
            ):
                assertpy_self.error(
                    f"Expected {assertpy_self.val} to be equal to {expected_model}, "
                    f"excluding fields '{excluded_fields}' but was not."
                )
            return assertpy_self

    @staticmethod
    def contains_only_models(assertpy_self, list_expected_model: List, excluded_fields: [str] = None):
        if not all(isinstance(el, BaseModel) for el in assertpy_self.val) or not all(
            isinstance(el, BaseModel) for el in list_expected_model
        ):
            raise ValueError("compared lists should contain items that inherit pydantic BaseModel")
        if len(assertpy_self.val) == 0 or len(list_expected_model) == 0:
            raise ValueError("lists must have elements")
        with allure.step(
            f"Asserting that list contains models that has all fields equal excluding '{excluded_fields or ''}' "
        ):
            excluded_fields = excluded_fields or []
            fields_to_compare = [
                attr for attr in list_expected_model[0].schema()["properties"].keys() if attr not in excluded_fields
            ]

            def compare_fields(expected, actual):
                return all([(getattr(actual, attr) == getattr(expected, attr)) for attr in fields_to_compare])

            extra = []
            for item in assertpy_self.val:
                if not list(filter(lambda expected: compare_fields(expected, item), list_expected_model)):
                    extra.append(item)
            if extra:
                assertpy_self.error(
                    "Expected <%s> to contain only %s, but did contain %s."
                    % (
                        assertpy_self.val,
                        assertpy_self._fmt_items(list_expected_model),
                        assertpy_self._fmt_items(extra),
                    )
                )

            missing = []
            for item in list_expected_model:
                if not list(filter(lambda expected: compare_fields(expected, item), assertpy_self.val)):
                    missing.append(item)
            if missing:
                assertpy_self.error(
                    "Expected <%s> to contain only %s, but did not contain %s."
                    % (
                        assertpy_self.val,
                        assertpy_self._fmt_items(list_expected_model),
                        assertpy_self._fmt_items(missing),
                    )
                )
            return assertpy_self

    @staticmethod
    def is_all_strings_has_value(assertpy_self):
        with allure.step("Asserting that all items in list not empty or none"):
            if not all([item is not None and len(assertpy_self.val) > 0 for item in assertpy_self.val]):
                assertpy_self.error("not all strings in list has value")
            return assertpy_self

    @staticmethod
    def has_length_greater_than(assertpy_self, length):
        with allure.step(f"Asserting that length is greater than {length}"):
            if len(assertpy_self.val) <= length:
                assertpy_self.error(f"length is not greater than {length}")
            return assertpy_self

    @staticmethod
    def _wrap_allure_step(func):
        @wraps(func)
        def wrapper(*args):
            limit = settings.assertpy_argument_length_limit
            main_argument = str(args[0].val)
            trimmed_main_argument = main_argument[:limit] + "..." if len(main_argument) > limit else main_argument
            secondary_argument = f'{" ,".join(map(str, args[1::]))}' if len(args) > 1 else ""
            trimmed_secondary_argument = (
                secondary_argument[:limit] + "..." if len(secondary_argument) > limit else str(secondary_argument)
            )

            step_description = (
                f"Asserting that \"{trimmed_main_argument}\" {func.__name__.replace('_', ' ')}"
                f' "{trimmed_secondary_argument}"'
            )

            with allure.step(step_description):
                allure.attach(main_argument, name="main argument", attachment_type=allure.attachment_type.TEXT)
                if secondary_argument:
                    allure.attach(
                        secondary_argument, name="secondary argument", attachment_type=allure.attachment_type.TEXT
                    )
                return func(*args)

        return wrapper

    @staticmethod
    def _wrap_assertpy_with_allure_step():
        for attr, val in AssertionBuilder.__dict__.items():
            if callable(val) and not attr.startswith("_"):
                setattr(AssertionBuilder, attr, AssertPyExtensions._wrap_allure_step(val))

        for base_class in AssertionBuilder.__bases__:
            for attr, val in base_class.__dict__.items():
                if callable(val) and not attr.startswith("_"):
                    setattr(base_class, attr, AssertPyExtensions._wrap_allure_step(val))
