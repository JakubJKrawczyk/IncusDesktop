from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class StepStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    DONE = "done"
    FAILED = "failed"
    SKIPPED = "skipped"


class StepResult(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str
    status: StepStatus = StepStatus.PENDING
    started_at: datetime | None = None
    finished_at: datetime | None = None
    error: str | None = None
    detail: dict[str, Any] = Field(default_factory=dict)


class ScenarioRun(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    scenario: str
    target: str | None = None
    status: StepStatus = StepStatus.RUNNING
    started_at: datetime
    finished_at: datetime | None = None
    steps: list[StepResult] = Field(default_factory=list)
    result: dict[str, Any] | None = None
    error: str | None = None
