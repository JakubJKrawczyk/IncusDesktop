from pydantic import BaseModel, ConfigDict


class CertificateModel(BaseModel):
    model_config = ConfigDict(extra="allow")

    fingerprint: str | None = None
    certificate: str | None = None
    name: str | None = None
    type: str | None = None
    description: str | None = None
    restricted: bool | None = None
    projects: list[str] | None = None
