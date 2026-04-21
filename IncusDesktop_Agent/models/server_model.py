from typing import Any

from pydantic import BaseModel, ConfigDict


class ServerEnvironment(BaseModel):
    model_config = ConfigDict(extra="allow")

    addresses: list[str] | None = None
    architectures: list[str] | None = None
    certificate: str | None = None
    certificate_fingerprint: str | None = None
    driver: str | None = None
    driver_version: str | None = None
    firewall: str | None = None
    kernel: str | None = None
    kernel_architecture: str | None = None
    kernel_features: dict[str, Any] | None = None
    kernel_version: str | None = None
    lxc_features: dict[str, Any] | None = None
    os_name: str | None = None
    os_version: str | None = None
    project: str | None = None
    server: str | None = None
    server_clustered: bool | None = None
    server_event_mode: str | None = None
    server_name: str | None = None
    server_pid: int | None = None
    server_version: str | None = None
    storage: str | None = None
    storage_version: str | None = None
    storage_supported_drivers: list[dict[str, Any]] | None = None


class ServerModel(BaseModel):
    model_config = ConfigDict(extra="allow")

    api_extensions: list[str] | None = None
    api_status: str | None = None
    api_version: str | None = None
    auth: str | None = None
    public: bool | None = None
    auth_methods: list[str] | None = None
    environment: ServerEnvironment | None = None
    config: dict[str, Any] | None = None
