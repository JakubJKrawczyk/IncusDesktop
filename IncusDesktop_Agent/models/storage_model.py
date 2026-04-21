from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class StoragePoolModel(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str | None = None
    description: str | None = None
    driver: str | None = None
    status: str | None = None
    locations: list[str] | None = None
    config: dict[str, Any] | None = None
    used_by: list[str] | None = None


class StoragePoolResources(BaseModel):
    model_config = ConfigDict(extra="allow")

    space: dict[str, Any] | None = None
    inodes: dict[str, Any] | None = None


class StorageVolumeModel(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str | None = None
    description: str | None = None
    type: str | None = None
    content_type: str | None = None
    pool: str | None = None
    location: str | None = None
    project: str | None = None
    created_at: datetime | None = None
    config: dict[str, Any] | None = None
    used_by: list[str] | None = None


class StorageVolumeState(BaseModel):
    model_config = ConfigDict(extra="allow")

    usage: dict[str, Any] | None = None


class StorageVolumeSnapshot(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str | None = None
    description: str | None = None
    created_at: datetime | None = None
    expires_at: datetime | None = None
    config: dict[str, Any] | None = None
    content_type: str | None = None


class StorageVolumeBackup(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str | None = None
    created_at: datetime | None = None
    expires_at: datetime | None = None
    volume_only: bool | None = None
    optimized_storage: bool | None = None


class StorageVolumeBitmap(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str | None = None


class StorageBucketModel(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str | None = None
    description: str | None = None
    pool: str | None = None
    s3_url: str | None = None
    location: str | None = None
    project: str | None = None
    config: dict[str, Any] | None = None
    used_by: list[str] | None = None


class StorageBucketKey(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str | None = None
    description: str | None = None
    role: str | None = None
    access_key: str | None = None
    secret_key: str | None = None


class StorageBucketBackup(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str | None = None
    created_at: datetime | None = None
    expires_at: datetime | None = None
