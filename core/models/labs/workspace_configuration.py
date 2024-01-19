from enum import StrEnum

from pydantic import BaseModel, Field

from util.random import random_string


def get_vm_name():
    return random_string(prefix="vm_name")


class ComponentType(StrEnum):
    VIRTUAL_MACHINE = "virtual_machine"
    SAAS = "saas"
    CODING = "coding"
    JUPYTER = "jupyter"


class WorkspaceConfigurationInput(BaseModel):
    """
    example = {
          "configuration_items": [],
          "name": "some_name",
        }
    """

    configuration_items: list = []
    name: str = Field(default_factory=random_string)


class WorkspaceConfiguration(WorkspaceConfigurationInput):
    """
    example = {
          "id": "wcfg-wqd2kgjav",
          "configuration_items": [],
          "name": None,
          "created_at": "2021-12-24T06:23:33.085166Z",
          "created_by": 1866,
          "last_used_at": "2021-12-24T06:23:33.081409Z",
          "organization": "org-mfyir3gna"
        }
    """

    id: str
    configuration_items: list
    name: str
    created_at: str
    created_by: int
    last_used_at: str
    organization: str


class WorkspaceConfigurationItemInput(BaseModel):
    component_type: ComponentType = ComponentType.VIRTUAL_MACHINE
    configuration: str
    image_id: str
    component_name: str = Field(default_factory=get_vm_name)
    virtual_network_id: str | None


class WorkspaceConfigurationItemUpdate(BaseModel):
    component_type: ComponentType = ComponentType.VIRTUAL_MACHINE
    configuration: str
    image_id: str
    component_name: str = Field(default_factory=get_vm_name)


class WorkspaceConfigurationItem(BaseModel):
    id: str
    component_type: ComponentType
    component_id: str
    configuration: str
    component_name: str
    component_labels: list
    image: dict
    created_at: str
    steps: list
    project_config: str | None


class WorkspaceStatuses(StrEnum):
    PREPARED = "prepared"
    PENDING = "pending"
    READY = "ready"
    FAILED = "failed"
    SUSPENDED = "suspended"
    DELETED = "deleted"


class Workspace(BaseModel):
    id: str
    status: WorkspaceStatuses
    created_at: str
    updated_at: str
    user: dict
    vms: dict
    projects: dict
    jupyter: dict
