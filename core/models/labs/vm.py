from enum import StrEnum

from pydantic import BaseModel

from core.models.labs.image import CommonImage


class VMStatuses(StrEnum):
    NONE = "none"
    PENDING = "pending"
    DEPLOYING = "deploying"
    RUNNING = "running"
    FAILED = "failed"
    SUSPENDED = "suspended"
    DELETED = "deleted"
    SUSPENDING = "suspending"
    RESETTING = "resetting"
    DELETING = "deleting"
    RESTARTING = "restarting"


class ExternalVM(BaseModel):
    """
    example = {'id': 'vm-wlk10ebjr',
     'image': {'id': 'img-ko3zkwk2m', 'created_at': '2020-08-03T04:30:05.514393Z',
               'updated_at': '2022-02-12T18:12:37.104120Z', 'system_status': 'active',
               'name': 'ubuntu20-selenium', 'type': 'base', 'provider': 'gce', 'system': 'linux',
               'os_type': 'Linux', 'os_version': 'Ubuntu 20.04', 'description': '', 'software': '',
               'is_ready': True, 'external_id': 'ubuntu-20-pkr-v1-4', 'deleted': False,
               'container_envs': {}, 'options': {'image_project': 'dev-alemira'},
               'organization': None, 'env_provider': 'env-osneg5yub'},
     'organization': 'org-mfyir3gna',
     'provider': 'gce',
     'region': 'none',
     'status': 'pending',
     'created_at': '2023-09-25T10:55:05.456365Z',
     'updated_at': '2023-09-25T10:55:05.490168Z',
     'ip': None,
     'private_ips': [],
     'ips': [],
     'component': None,
     'sessions': None}
    """

    id: str
    image: CommonImage
    organization: str
    provider: str
    region: str
    status: VMStatuses
    created_at: str
    updated_at: str
    ip: str | None
    private_ips: list[str] | None
    ips: list[str] | None
    component: str | None
    sessions: None


class ExternalVMInput(BaseModel):
    image_id: str
