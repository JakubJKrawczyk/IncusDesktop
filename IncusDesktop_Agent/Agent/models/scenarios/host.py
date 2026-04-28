from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class HostBootstrapSpec(BaseModel):
    model_config = ConfigDict(extra="allow")

    storage_pool_name: str = "default"
    storage_pool_driver: str = "dir"
    storage_pool_config: dict[str, Any] = Field(default_factory=dict)
    network_name: str = "incusbr0"
    network_type: str = "bridge"
    network_config: dict[str, Any] = Field(default_factory=dict)
    attach_to_default_profile: bool = True


class ProjectBootstrapSpec(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str
    description: str | None = None
    config: dict[str, Any] = Field(default_factory=dict)
    create_default_profile: bool = True
    profile_config: dict[str, Any] = Field(default_factory=dict)
    profile_devices: dict[str, dict[str, Any]] = Field(default_factory=dict)
