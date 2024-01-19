import http
from typing import Type

import assertpy

from util.assertions import common_assertions


class BaseApiTest:
    # the staticmethod function breaks autocompletion, so we must repeat it as
    # function: Type[...] = ...

    assert_that: Type[assertpy.assert_that] = staticmethod(assertpy.assert_that)
    assert_response_status: Type[common_assertions.assert_response_status] = staticmethod(
        common_assertions.assert_response_status
    )
    soft_assertions: Type[assertpy.soft_assertions] = staticmethod(assertpy.soft_assertions)
    http = http.HTTPStatus
