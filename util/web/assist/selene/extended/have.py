from selene.support.conditions.have import *

from util.web.assist.selene.extended import match


def url_path_matching(value: str) -> Condition[Browser]:
    return match.browser_has_url_path(value)
