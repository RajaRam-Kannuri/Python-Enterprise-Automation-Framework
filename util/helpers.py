from collections.abc import Iterable
from datetime import UTC, datetime, timedelta
from typing import TypeVar
from urllib.parse import parse_qs, urlparse

from assertpy import assert_that
from bs4 import Tag


def get_string_after_separator(string, seperator):
    return string.split(seperator)[-1]


def get_query_parameter(url, parameter_name):
    parsed_url = urlparse(url)
    query_parameters = parse_qs(parsed_url.query)
    parameter_value = query_parameters.get(parameter_name, [None])[0]

    return parameter_value


def extract_value_from_html(html: Tag, name: str) -> str:
    element = html.find(attrs={"name": name})
    if element is not None:
        return element.get("value")
    return ""


def get_date_with_offset(days: int = 0) -> datetime:
    now = datetime.now(UTC).replace(microsecond=0, second=0)
    new_date = now + timedelta(days=days)
    return new_date


T = TypeVar("T")


def first(iterable: Iterable[T]) -> T | None:
    return next(iter(iterable), None)


def verify_activity_part_report(
    activity_part_reports, parent_id=None, order=None, activity_type=None, average_score=None
):
    matching_reports = [
        activity_part
        for activity_part in activity_part_reports.data
        if (parent_id is None or activity_part.parent_id == parent_id)
        and (order is None or activity_part.order == order)
    ]

    assert_that(matching_reports).described_as("No matching activity part report found").is_true()

    activity_part_report = matching_reports[0]

    assert_that(activity_part_report.activity.type).described_as(
        f"Activity type should be reported {activity_type}"
    ).is_equal_to(activity_type)
    assert_that(activity_part_report.order).described_as(f"Activity order should be reported {order}").is_equal_to(
        order
    )
    assert_that(activity_part_report.average_score).described_as(
        f"Average score should be reported {average_score}"
    ).is_equal_to(average_score)
