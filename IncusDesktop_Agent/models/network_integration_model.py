from typing import Any

from pydantic import BaseModel, ConfigDict


class NetworkIntegrationModel(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str | None = None
    description: str | None = None
    type: str | None = None
    config: dict[str, Any] | None = None
    used_by: list[str] | None = None
