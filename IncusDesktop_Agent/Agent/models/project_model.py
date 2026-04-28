from typing import Any

from pydantic import BaseModel, ConfigDict


class ProjectModel(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str | None = None
    description: str | None = None
    config: dict[str, Any] | None = None
    used_by: list[str] | None = None


class ProjectState(BaseModel):
    model_config = ConfigDict(extra="allow")

    resources: dict[str, Any] | None = None
