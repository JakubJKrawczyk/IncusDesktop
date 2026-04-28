from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

class OperationModel(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    class_: str | None = Field(default=None, alias="class")
    description: str | None = None
    status: str | None = None
    status_code: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    err: str | None = None
    may_cancel: bool | None = None
    location: str | None = None
    resources: dict[str, list[str]] | None = None
    metadata: dict[str, Any] | None = None