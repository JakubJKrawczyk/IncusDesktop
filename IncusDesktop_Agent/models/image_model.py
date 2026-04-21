from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class ImageAliasModel(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str | None = None
    description: str | None = None
    target: str | None = None
    type: str | None = None


class ImageSource(BaseModel):
    model_config = ConfigDict(extra="allow")

    alias: str | None = None
    certificate: str | None = None
    fingerprint: str | None = None
    mode: str | None = None
    protocol: str | None = None
    secret: str | None = None
    server: str | None = None
    type: str | None = None
    url: str | None = None


class ImageMetadata(BaseModel):
    model_config = ConfigDict(extra="allow")

    architecture: str | None = None
    creation_date: int | None = None
    expiry_date: int | None = None
    properties: dict[str, Any] | None = None
    templates: dict[str, Any] | None = None


class ImageModel(BaseModel):
    model_config = ConfigDict(extra="allow")

    fingerprint: str | None = None
    aliases: list[ImageAliasModel] | None = None
    auto_update: bool | None = None
    cached: bool | None = None
    created_at: datetime | None = None
    expires_at: datetime | None = None
    filename: str | None = None
    last_used_at: datetime | None = None
    architecture: str | None = None
    profiles: list[str] | None = None
    properties: dict[str, Any] | None = None
    public: bool | None = None
    size: int | None = None
    type: str | None = None
    uploaded_at: datetime | None = None
    update_source: ImageSource | None = None
    project: str | None = None
