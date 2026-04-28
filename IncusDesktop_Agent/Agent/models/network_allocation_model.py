from pydantic import BaseModel, ConfigDict


class NetworkAllocationModel(BaseModel):
    model_config = ConfigDict(extra="allow")

    address: str | None = None
    used_by: str | None = None
    type: str | None = None
    hwaddr: str | None = None
    network: str | None = None
    nat: bool | None = None
    project: str | None = None
