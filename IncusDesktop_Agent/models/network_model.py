from typing import Any

from pydantic import BaseModel, ConfigDict


class NetworkModel(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str | None = None
    description: str | None = None
    type: str | None = None
    managed: bool | None = None
    status: str | None = None
    locations: list[str] | None = None
    config: dict[str, Any] | None = None
    used_by: list[str] | None = None
    project: str | None = None


class NetworkState(BaseModel):
    model_config = ConfigDict(extra="allow")

    addresses: list[dict[str, Any]] | None = None
    counters: dict[str, Any] | None = None
    hwaddr: str | None = None
    mtu: int | None = None
    state: str | None = None
    type: str | None = None
    bond: dict[str, Any] | None = None
    bridge: dict[str, Any] | None = None
    vlan: dict[str, Any] | None = None
    ovn: dict[str, Any] | None = None


class NetworkLease(BaseModel):
    model_config = ConfigDict(extra="allow")

    hostname: str | None = None
    address: str | None = None
    hwaddr: str | None = None
    type: str | None = None
    location: str | None = None
    project: str | None = None


class NetworkForwardPort(BaseModel):
    model_config = ConfigDict(extra="allow")

    description: str | None = None
    protocol: str | None = None
    listen_port: str | None = None
    target_address: str | None = None
    target_port: str | None = None
    snat: bool | None = None


class NetworkForward(BaseModel):
    model_config = ConfigDict(extra="allow")

    listen_address: str | None = None
    description: str | None = None
    config: dict[str, Any] | None = None
    ports: list[NetworkForwardPort] | None = None
    location: str | None = None


class NetworkLoadBalancerBackend(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str | None = None
    description: str | None = None
    target_address: str | None = None
    target_port: str | None = None


class NetworkLoadBalancerPort(BaseModel):
    model_config = ConfigDict(extra="allow")

    description: str | None = None
    protocol: str | None = None
    listen_port: str | None = None
    target_backend: list[str] | None = None


class NetworkLoadBalancer(BaseModel):
    model_config = ConfigDict(extra="allow")

    listen_address: str | None = None
    description: str | None = None
    config: dict[str, Any] | None = None
    backends: list[NetworkLoadBalancerBackend] | None = None
    ports: list[NetworkLoadBalancerPort] | None = None
    location: str | None = None


class NetworkLoadBalancerState(BaseModel):
    model_config = ConfigDict(extra="allow")

    backend_health: dict[str, Any] | None = None


class NetworkPeer(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str | None = None
    description: str | None = None
    config: dict[str, Any] | None = None
    target_project: str | None = None
    target_network: str | None = None
    target_integration: str | None = None
    type: str | None = None
    status: str | None = None
    used_by: list[str] | None = None
