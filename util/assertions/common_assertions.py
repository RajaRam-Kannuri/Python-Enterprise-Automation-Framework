import allure
from assertpy import assert_that


def assert_response_status(actual, expected):
    with allure.step(f"Asserting response status code to be {expected}"):
        assert_that(actual).is_equal_to(expected)
