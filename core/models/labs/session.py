from enum import StrEnum

from pydantic import BaseModel

from core.models.labs.workspace_configuration import Workspace


class Object(BaseModel):
    id: str
    name: str


class SessionInput(BaseModel):
    lab_id: str
    meta: dict = {}
    is_service: bool = True


class SessionStates(StrEnum):
    PREPARED = "prepared"
    ACTIVE = "active"
    FINISHED = "finished"
    INREVIEW = "inreview"
    PAUSED = "paused"
    CLEANED = "cleaned"


class Session(BaseModel):
    """
    example =
            {'id': 'ses-btxk36vyg', 'lab': {'id': '2447', 'name': 'AUTOTESTDl1S5G41Xw'},
         'user': {'id': 1866, 'email': 'autotest@alemira.dev', 'first_name': 'Test', 'last_name': 'Testovich',
                  'picture_url': '', 'locale': None},
         'workspace': {'id': 'wksc-9cyymyxpm', 'status': 'prepared', 'created_at': '2023-08-11T09:08:55.918514Z',
                       'updated_at': '2023-08-11T09:08:55.918537Z',
                       'user': {'id': 1866, 'email': 'autotest@alemira.dev', 'first_name': 'Test',
                                'last_name': 'Testovich',
                                'picture_url': '', 'locale': None},
                       'vms': [{'id': 'vm-pqf1efj0f',
                                 'image': {'id': 'img-ko3zkwk2m',
                                           'created_at': '2020-08-03T04:30:05.514393Z',
                                           'updated_at': '2022-02-12T18:12:37.104120Z',
                                           'system_status': 'active',
                                           'name': 'ubuntu20-selenium',
                                           'type': 'base', 'provider': 'gce',
                                           'system': 'linux', 'os_type': 'Linux',
                                           'os_version': 'Ubuntu 20.04',
                                           'description': '', 'software': '',
                                           'is_ready': True,
                                           'external_id': 'ubuntu-20-pkr-v1-4',
                                           'deleted': False, 'container_envs': {},
                                           'options': {
                                               'image_project': 'dev-alemira'},
                                           'organization': None,
                                           'env_provider': 'env-osneg5yub'},
                                 'organization': 'org-mfyir3gna', 'provider': 'gce',
                                 'region': 'none', 'status': 'none',
                                 'created_at': '2023-08-11T09:08:55.933549Z',
                                 'updated_at': '2023-08-11T09:08:55.933572Z',
                                 'ip': None, 'private_ips': [], 'ips': [],
                                 'component': {'id': 'cmp-hsv6vaey1',
                                               'name': 'vm_nameFI97mhLQhZ',
                                               'type': 'virtual_machine',
                                               'created_at': '2023-08-11T09:08:08.885344Z',
                                               'labels': []}}], 'projects': [],
                       'jupyter': []},
         'state': 'prepared',
         'created_at': '2023-08-11T09:08:55.956767Z',
         'updated_at': '2023-08-11T09:08:55.959915Z',
         'started_at': None,
         'finished_at': None,
         'meta': {'limit_seconds': 3600, 'api_token': 'VarSessionToken 83abcdc1a9'},
         'is_service': True,
         'ready_at': None,
         'lab_type': 'virtual_machine'}
    """

    id: str
    lab: Object
    user: dict
    workspace: Workspace
    state: SessionStates
    created_at: str
    updated_at: str | None
    started_at: str | None
    finished_at: str | None
    meta: dict
    ready_at: str | None
    lab_type: str | None
    is_service: bool
