from typing import Any

from pydantic import BaseModel, ConfigDict


class NetworkACLRule(BaseModel):
    model_config = ConfigDict(extra="allow")

    action: str | None = None
    source: str | None = None
    destination: str | None = None
    protocol: str | None = None
    source_port: str | None = None
    destination_port: str | None = None
    icmp_type: str | None = None
    icmp_code: str | None = None
    description: str | None = None
    state: str | None = None


class NetworkACLModel(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str | None = None
    description: str | None = None
    config: dict[str, Any] | None = None
    egress: list[NetworkACLRule] | None = None
    ingress: list[NetworkACLRule] | None = None
    used_by: list[str] | None = None
    project: str | None = None
