from enum import StrEnum

from pydantic import BaseModel


class SupportedNetworks(StrEnum):
    PUBLIC = "PUBLIC"
    SECURE = "SECURE"


class Network(BaseModel):
    """
    example = {id: 478, firewall_rules_type: "PUBLIC"}
    """

    id: int
    firewall_rules_type: str = SupportedNetworks


class NetworkInput(BaseModel):
    virtual_network_id: int


class ExternalImageProvider(StrEnum):
    GCE = "gce"
