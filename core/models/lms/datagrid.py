from datetime import datetime

from pydantic import Field

from core.models.lms.lms_base import LMSEntityModelBase, LMSModelBase


class DataGridFilterPanel(LMSModelBase):
    filter_enabled: bool = False


class DataGridColumn(LMSModelBase):
    name: str
    data_type: str | None
    data_field: str | None
    visible: bool
    visible_index: int | None


class DataGridProperties(LMSModelBase):
    """
    Class describing datagrid settings pushed as string indo db.
    Docs - https://js.devexpress.com/DevExtreme/ApiReference/UI_Components/dxDataGrid/
    Code - https://github.com/DevExpress/DevExtreme/blob/23_1/js/ui/data_grid.d.ts#L677
    """

    page_index: int | None = 0
    page_size: int | None = 1
    allowed_page_sizes: list[int] | None = [1, 2, 3]
    filter_panel: DataGridFilterPanel | None = DataGridFilterPanel()
    filter_value: str = ""
    selected_row_keys: list[int] | None = Field(default_factory=list)
    search_text: str = ""
    columns: list[DataGridColumn] = Field(default_factory=list)


class CreateDataGridSetting(LMSModelBase):
    key: str = Field(default_factory=lambda: f"test-key-{int(datetime.now().timestamp())}")
    settings: str = DataGridProperties().json(by_alias=True)


class DataGridSetting(LMSEntityModelBase):
    id: str
    key: str
    settings: str
    user_id: str
