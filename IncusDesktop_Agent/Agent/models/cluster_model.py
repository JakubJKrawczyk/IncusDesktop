from typing import Any

from pydantic import BaseModel, ConfigDict


class ClusterInfo(BaseModel):
    model_config = ConfigDict(extra="allow")

    server_name: str | None = None
    enabled: bool | None = None
    member_config: list[dict[str, Any]] | None = None


class ClusterMember(BaseModel):
    model_config = ConfigDict(extra="allow")

    server_name: str | None = None
    url: str | None = None
    database: bool | None = None
    status: str | None = None
    message: str | None = None
    architecture: str | None = None
    failure_domain: str | None = None
    description: str | None = None
    config: dict[str, Any] | None = None
    groups: list[str] | None = None
    roles: list[str] | None = None


class ClusterMemberState(BaseModel):
    model_config = ConfigDict(extra="allow")

    sysinfo: dict[str, Any] | None = None
    storage_pools: dict[str, Any] | None = None


class ClusterGroup(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str | None = None
    description: str | None = None
    members: list[str] | None = None
