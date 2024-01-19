import allure

from core.api.base import ApiObjectManager, DeletableApiObject
from core.api.base_api import ObjectCreatableApi, ObjectDeleteableApi, ObjectGettableApi, ObjectNotFound
from core.models.lms.datagrid import CreateDataGridSetting
from core.models.lms.datagrid import DataGridSetting as DataGridSettingModel
from settings import settings


class DatagridSettingsApi(
    ObjectCreatableApi[CreateDataGridSetting, DataGridSettingModel],
    ObjectGettableApi[DataGridSettingModel],
    ObjectDeleteableApi,
):
    NAME = "Datagrid settings"
    PATH_NAME = "datagrid-settings"
    URL = f"{settings.base_url_lms_api}{PATH_NAME}"
    MODEL = DataGridSettingModel


class DataGridSetting(DeletableApiObject[DataGridSettingModel, DatagridSettingsApi]):
    API = DatagridSettingsApi

    @property
    def id(self) -> str:
        return self.data.key

    def teardown(self):
        try:
            self.delete()
        except ObjectNotFound:
            pass


class DataGridSettingManager(ApiObjectManager):
    API = DatagridSettingsApi
    OBJECT = DataGridSetting

    def create(self, *, key: str | None = None, settings: str | None = None) -> DataGridSetting:
        create_data = CreateDataGridSetting()
        if key:
            create_data.key = key
        if settings:
            create_data.settings = settings

        with allure.step(f"Create Datagrid Settings object with key {key}"):
            data = self._api.post(create_data)
            return DataGridSetting(self.session, data)
