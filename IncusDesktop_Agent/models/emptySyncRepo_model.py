

# app/models/responses.py
from pydantic import BaseModel, ConfigDict



class EmptySyncResponse(BaseModel):
    """
    Envelope sync bez metadata. Zwracany przez endpointy typu PATCH /instances/{name}
    ktore kończą sie sukcesem ale nie maja body do oddania.

    JSON wyglada tak:
        {"type": "sync", "status": "Success", "status_code": 200}
    """

    model_config = ConfigDict(extra="allow")

    type: str | None = None          # zawsze "sync"
    status: str | None = None        # zawsze "Success"
    status_code: int | None = None  # zawsze 200