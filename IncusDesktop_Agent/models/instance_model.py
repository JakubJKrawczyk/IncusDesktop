# app/models/instance.py
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field



# ─── InstanceState sub-models ──────────────────────────────────────────────

class InstanceStateCPU(BaseModel):
    model_config = ConfigDict(extra="allow")

    allocated_time: int | None = None  # ns/s dostepne dla CPU
    usage: int | None = None           # skumulowany czas CPU w ns


class InstanceStateMemory(BaseModel):
    model_config = ConfigDict(extra="allow")

    total: int | None = None            # bytes
    usage: int | None = None            # bytes
    usage_peak: int | None = None
    swap_usage: int | None = None
    swap_usage_peak: int | None = None


class InstanceStateDisk(BaseModel):
    model_config = ConfigDict(extra="allow")

    total: int | None = None  # bytes
    usage: int | None = None  # bytes


class InstanceStateOSInfo(BaseModel):
    model_config = ConfigDict(extra="allow")

    os: str | None = None
    os_version: str | None = None
    kernel_version: str | None = None
    hostname: str | None = None
    fqdn: str | None = None


class InstanceStateNetworkAddress(BaseModel):
    model_config = ConfigDict(extra="allow")

    family: str | None = None   # "inet" | "inet6"
    address: str | None = None
    netmask: str | None = None  # uwaga: STRING w Incus ("64", "24"), nie int
    scope: str | None = None    # "local" | "link" | "global"


class InstanceStateNetworkCounters(BaseModel):
    model_config = ConfigDict(extra="allow")

    bytes_received: int | None = None
    bytes_sent: int | None = None
    packets_received: int | None = None
    packets_sent: int | None = None
    errors_received: int | None = None
    errors_sent: int | None = None
    packets_dropped_inbound: int | None = None
    packets_dropped_outbound: int | None = None


class InstanceStateNetwork(BaseModel):
    model_config = ConfigDict(extra="allow")

    type: str | None = None       # "broadcast" | "loopback" | "point-to-point" | ...
    state: str | None = None      # "up" | "down"
    hwaddr: str | None = None     # MAC
    host_name: str | None = None  # interfejs po stronie hosta (np. vethXXX)
    mtu: int | None = None
    addresses: list[InstanceStateNetworkAddress] | None = None
    counters: InstanceStateNetworkCounters | None = None


# ─── InstanceState ─────────────────────────────────────────────────────────

class InstanceState(BaseModel):
    model_config = ConfigDict(extra="allow")

    status: str | None = None  # "Running" | "Stopped" | "Frozen" | "Error"
    status_code: int | None = None
    pid: int | None = None
    processes: int | None = None
    started_at: datetime | None = None

    cpu: InstanceStateCPU | None = None
    memory: InstanceStateMemory | None = None
    os_info: InstanceStateOSInfo | None = None

    # key = nazwa interfejsu ("eth0", "lo"), key = nazwa device'a ("root")
    network: dict[str, InstanceStateNetwork] | None = None
    disk: dict[str, InstanceStateDisk] | None = None


# ─── InstanceSnapshot ──────────────────────────────────────────────────────

class InstanceSnapshot(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str | None = None
    architecture: str | None = None

    created_at: datetime | None = None
    last_used_at: datetime | None = None
    expires_at: datetime | None = None  # auto-delete

    ephemeral: bool | None = None
    stateful: bool | None = None
    size: int | None = None  # bytes

    profiles: list[str] | None = None
    config: dict[str, Any] | None = None
    devices: dict[str, Any] | None = None
    expanded_config: dict[str, Any] | None = None
    expanded_devices: dict[str, Any] | None = None


# ─── InstanceBackup ────────────────────────────────────────────────────────

class InstanceBackup(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str | None = None
    created_at: datetime | None = None
    expires_at: datetime | None = None
    instance_only: bool | None = None      # bez snapshotow
    optimized_storage: bool | None = None  # pool-native format zamiast tarballa


# ─── InstanceFull ──────────────────────────────────────────────────────────

class InstanceModel(BaseModel):
    """Pelna reprezentacja instancji (recursion=1): Instance + state + snapshots + backups."""

    model_config = ConfigDict(extra="allow")

    name: str | None = None
    description: str | None = None
    type: str | None = None  # "container" | "virtual-machine"
    architecture: str | None = None
    status: str | None = None
    status_code: int | None = None

    project: str | None = None
    location: str | None = None
    created_at: datetime | None = None
    last_used_at: datetime | None = None

    ephemeral: bool | None = None
    stateful: bool | None = None
    disk_only: bool | None = None
    restore: str | None = None

    config: dict[str, Any] | None = None
    devices: dict[str, Any] | None = None
    expanded_config: dict[str, Any] | None = None
    expanded_devices: dict[str, Any] | None = None

    profiles: list[str] | None = None

    state: InstanceState | None = None
    snapshots: list[InstanceSnapshot] | None = Field(default=None)
    backups: list[InstanceBackup] | None = Field(default=None)