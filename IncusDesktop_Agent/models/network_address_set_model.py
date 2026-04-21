from typing import Any

from pydantic import BaseModel, ConfigDict


class NetworkAddressSetModel(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str | None = None
    description: str | None = None
    addresses: list[str] | None = None
    config: dict[str, Any] | None = None
    used_by: list[str] | None = None
    project: str | None = None
