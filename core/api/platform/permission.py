from core.api.base_api import ObjectCreatableApi, ObjectDeleteableApi, ObjectQueryableApi
from core.api.platform.base import PlatformGettableApi
from core.models.platform.permission import CreatePermission, Permission
from settings import settings


class PermissionsApi(
    PlatformGettableApi[Permission],
    ObjectQueryableApi[Permission],
    ObjectCreatableApi[CreatePermission, Permission],
    ObjectDeleteableApi,
):
    NAME = "Permissions"
    PATH_NAME = "permissions"
    URL = f"{settings.base_url_platform_api}{PATH_NAME}"
    MODEL = Permission
