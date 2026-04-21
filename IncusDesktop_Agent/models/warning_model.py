from datetime import datetime

from pydantic import BaseModel, ConfigDict


class WarningModel(BaseModel):
    model_config = ConfigDict(extra="allow")

    uuid: str | None = None
    type: str | None = None
    count: int | None = None
    entity_url: str | None = None
    first_seen_at: datetime | None = None
    last_seen_at: datetime | None = None
    last_message: str | None = None
    location: str | None = None
    project: str | None = None
    severity: str | None = None
    status: str | None = None
