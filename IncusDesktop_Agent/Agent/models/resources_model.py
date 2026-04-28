from typing import Any

from pydantic import BaseModel, ConfigDict


class ResourcesModel(BaseModel):
    model_config = ConfigDict(extra="allow")

    cpu: dict[str, Any] | None = None
    memory: dict[str, Any] | None = None
    gpu: dict[str, Any] | None = None
    network: dict[str, Any] | None = None
    storage: dict[str, Any] | None = None
    usb: dict[str, Any] | None = None
    pci: dict[str, Any] | None = None
    system: dict[str, Any] | None = None
    load: dict[str, Any] | None = None
