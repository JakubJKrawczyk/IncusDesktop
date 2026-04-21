
# app/models/access.py
from pydantic import BaseModel, ConfigDict


class AccessEntry(BaseModel):
    """Jeden wpis listy dostepu — kto i z jaka rola moze dotknac zasobu."""

    model_config = ConfigDict(extra="allow")

    identifier: str | None = None  # fingerprint certyfikatu lub nazwa usera (openfga)
    provider: str | None = None    # "tls" | "openfga"
    role: str | None = None        # "admin" | "view" | "operator"


# Alias dla spójnosci z nazewnictwem Incus API
Access = list[AccessEntry]