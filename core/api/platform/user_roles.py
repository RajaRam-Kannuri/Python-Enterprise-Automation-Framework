from core.api.base_api import ObjectCreatableApi
from core.api.platform.base import PlatformGettableApi
from core.models.platform.user_role import CreateUserRole, UserRole
from settings import settings


class UserRolesApi(
    PlatformGettableApi[UserRole],
    ObjectCreatableApi[CreateUserRole, UserRole],
):
    NAME = "User - role relation"
    PATH_NAME = "user-roles"
    URL = f"{settings.base_url_platform_api}{PATH_NAME}"
    MODEL = UserRole
