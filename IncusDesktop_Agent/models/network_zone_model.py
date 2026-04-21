from typing import Any

from pydantic import BaseModel, ConfigDict


class NetworkZoneModel(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str | None = None
    description: str | None = None
    config: dict[str, Any] | None = None
    used_by: list[str] | None = None
    project: str | None = None


class NetworkZoneRecordEntry(BaseModel):
    model_config = ConfigDict(extra="allow")

    type: str | None = None
    value: str | None = None
    ttl: int | None = None


class NetworkZoneRecordModel(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str | None = None
    description: str | None = None
    config: dict[str, Any] | None = None
    entries: list[NetworkZoneRecordEntry] | None = None
