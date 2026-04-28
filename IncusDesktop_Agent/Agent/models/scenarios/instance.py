from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ProvisionSpec(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str
    image_alias: str = "ubuntu/22.04"
    image_server: str = "https://images.linuxcontainers.org"
    image_protocol: str = "simplestreams"
    project: str = "default"
    instance_type: str = "container"  # "container" | "virtual-machine"
    profiles: list[str] = Field(default_factory=lambda: ["default"])
    cpu: int | None = None
    memory: str | None = None  # "2GB"
    root_disk_size: str | None = None  # "10GB"
    network: str | None = None  # NIC parent network name
    ssh_pubkey: str | None = None
    cloud_init_user_data: str | None = None
    start: bool = True
    wait_agent: bool = True
    wait_agent_timeout: int = 120
    extra_config: dict[str, Any] = Field(default_factory=dict)
    extra_devices: dict[str, dict[str, Any]] = Field(default_factory=dict)


class CloneSpec(BaseModel):
    model_config = ConfigDict(extra="allow")

    source_name: str
    target_name: str
    project: str = "default"
    target_project: str | None = None
    snapshot: str | None = None  # source snapshot to copy from
    instance_only: bool = False  # skip copying snapshots
    start: bool = True


class DecommissionSpec(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str
    project: str = "default"
    final_snapshot: bool = True
    final_snapshot_name: str | None = None
    force_stop: bool = True
    stop_timeout: int = 30


class RestartSpec(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str
    project: str = "default"
    timeout: int = 30
    force: bool = False


class ResetToSnapshotSpec(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str
    snapshot: str
    project: str = "default"
    start_after: bool = True


class ResourceUpdateSpec(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str
    project: str = "default"
    cpu: int | None = None
    memory: str | None = None
    root_disk_size: str | None = None
    restart_if_required: bool = True


class AttachVolumeSpec(BaseModel):
    model_config = ConfigDict(extra="allow")

    instance: str
    project: str = "default"
    pool: str
    volume: str
    create_if_missing: bool = False
    volume_size: str | None = None
    device_name: str | None = None  # default: same as volume name
    mount_path: str | None = None  # required for containers
    readonly: bool = False
    restart_instance: bool = False


class AttachNetworkSpec(BaseModel):
    model_config = ConfigDict(extra="allow")

    instance: str
    project: str = "default"
    network: str
    device_name: str | None = None  # default: "eth<N>"
    nic_type: str = "bridged"
    ipv4_address: str | None = None
    ipv6_address: str | None = None
    restart_instance: bool = False


class ExposePortSpec(BaseModel):
    model_config = ConfigDict(extra="allow")

    instance: str
    project: str = "default"
    network: str
    listen_address: str
    target_port: int
    listen_port: int | None = None  # defaults to target_port
    protocol: str = "tcp"
    description: str | None = None


class RunCommandSpec(BaseModel):
    model_config = ConfigDict(extra="allow")

    instance: str
    project: str = "default"
    command: list[str]
    user: int = 0
    group: int = 0
    cwd: str | None = None
    environment: dict[str, str] = Field(default_factory=dict)
    timeout_seconds: int = 60
    capture_output: bool = True


class SnapshotSpec(BaseModel):
    model_config = ConfigDict(extra="allow")

    instance: str
    project: str = "default"
    name: str | None = None  # default: timestamp
    stateful: bool = False
    expires_at: str | None = None  # RFC3339
    keep_last_n: int | None = None  # retention; prune older if set


class BackupExportSpec(BaseModel):
    model_config = ConfigDict(extra="allow")

    instance: str
    project: str = "default"
    name: str | None = None  # backup name; default: timestamp
    compression_algorithm: str | None = None  # "gzip" | "zstd" | ...
    optimized_storage: bool = False
    instance_only: bool = False


class RestoreFromBackupSpec(BaseModel):
    model_config = ConfigDict(extra="allow")

    project: str = "default"
    backup_name: str  # name in agent's local store / uploaded
    target_name: str | None = None  # rename after restore
    start_after: bool = False
