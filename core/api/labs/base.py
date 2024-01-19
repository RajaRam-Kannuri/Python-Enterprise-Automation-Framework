from typing import Generic, TypeVar

from pydantic import BaseModel

from core.api.base_refactored.api_wrapper import (
    ApiWrap,
    ApiWrapper,
    CreatablesManager,
    DataModel,
    DeletableWrapper,
    GettableWrapper,
    ManagerClient,
    PatchableWrapper,
    PuttableWrapper,
    QueryablesManager,
)

InputModel = TypeVar("InputModel", bound=BaseModel)


class LabsCommonObjectWrapper(
    DeletableWrapper[ApiWrap, DataModel],
    PatchableWrapper[ApiWrapper, DataModel, InputModel],
    PuttableWrapper[ApiWrapper, DataModel, InputModel],
    GettableWrapper[ApiWrap, DataModel],
    Generic[ApiWrap, DataModel, InputModel],
):
    ...


class LabsCommonManager(
    CreatablesManager[ManagerClient, ApiWrap, InputModel],
    QueryablesManager[ManagerClient, ApiWrap],
    Generic[ManagerClient, ApiWrap, InputModel],
):
    ...
