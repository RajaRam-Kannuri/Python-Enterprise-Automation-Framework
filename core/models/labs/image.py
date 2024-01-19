from enum import StrEnum

from pydantic import BaseModel, Field

from util.random import random_string


class ImageSystemStatus(StrEnum):
    active = "active"
    archived = "archived"
    blocked = "blocked"
    deleted = "deleted"


class EnvProvider(BaseModel):
    id: str
    name: str
    type: str


class SystemType(StrEnum):
    windows = "Windows"
    linux = "Linux"


class ExternalImageInput(BaseModel):
    system_status: ImageSystemStatus | None
    name: str = Field(default_factory=lambda: random_string(prefix="AUTOTEST_"))
    os_type: SystemType = SystemType.linux
    os_version: str = "Ubuntu 20.04"
    description: str = ""
    software: str = ""
    env_provider: EnvProvider | None


class ExternalImage(BaseModel):
    """example =
    {
      "id": "img-04nq6dfb3",
      "created_at": "2023-09-11T19:28:40.281323Z",
      "updated_at": "2023-09-11T19:28:40.284759Z",
      "system_status": "active",
      "name": "autotest cwwAYoSFPUQJRCtOnXxMWVmJgDvSzETKrQzlhlyRzzfVjrruIyqXpMAqfEvEmYFMo",
      "type": "custom",
      "provider": "gce",
      "system": "linux",
      "os_type": "Linux",
      "os_version": "Ubuntu 20.04",
      "description": "",
      "software": "",
      "is_ready": false,
      "external_id": "None",
      "deleted": false,
      "organization": "org-mfyir3gna",
      "used_labs_count": 0,
      "env_provider": {
        "id": "env-osneg5yub",
        "name": "Constructor Cloud",
        "type": "gce"
      }
    }
    """

    id: str
    created_at: str
    updated_at: str
    system_status: ImageSystemStatus
    name: str
    type: str
    provider: str
    system: str
    os_type: str
    os_version: str
    description: str | None
    software: str | None
    is_ready: bool
    external_id: str | None
    deleted: bool
    organization: str | None
    used_labs_count: int | None
    env_provider: EnvProvider


class CommonImage(BaseModel):
    """Used in ExternalVM
    example =
    {'id': 'img-ko3zkwk2m', 'created_at': '2020-08-03T04:30:05.514393Z',
     'updated_at': '2022-02-12T18:12:37.104120Z', 'system_status': 'active',
     'name': 'ubuntu20-selenium', 'type': 'base', 'provider': 'gce', 'system': 'linux',
     'os_type': 'Linux', 'os_version': 'Ubuntu 20.04', 'description': '', 'software': '',
     'is_ready': True, 'external_id': 'ubuntu-20-pkr-v1-4', 'deleted': False,
     'container_envs': {}, 'options': {'image_project': 'dev-alemira'},
     'organization': None, 'env_provider': 'env-osneg5yub'}
    """

    id: str
    created_at: str
    updated_at: str
    system_status: ImageSystemStatus
    name: str
    type: str
    provider: str
    system: str
    os_type: str
    os_version: str
    description: str | None
    software: str | None
    is_ready: bool
    external_id: str | None
    deleted: bool
    organization: str | None
    env_provider: str
    container_envs: dict | None
    options: dict | None
