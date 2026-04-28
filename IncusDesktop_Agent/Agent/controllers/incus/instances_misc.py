from Agent.models.operation_model import OperationModel
from Agent.utility.rest_client import IncusRestClient


class InstancesMiscController:
    def __init__(self, client: IncusRestClient):
        self._client = client

    # POST /1.0/instances/{name}/bitmaps (async)
    async def create_bitmap(self, name: str, body: dict, project: str = "default") -> OperationModel:
        return await self._client.post(
            f"/1.0/instances/{name}/bitmaps",
            json_body=body,
            params={"project": project},
        )

    # GET /1.0/instances/{name}/debug/memory (raw)
    async def debug_memory(self, name: str, format: str | None = None, project: str = "default") -> bytes:
        return await self._client.get(
            f"/1.0/instances/{name}/debug/memory",
            params={"format": format, "project": project},
            raw=True,
        )

    # GET /1.0/instances/{name}/debug/repair (sync)
    async def debug_repair(self, name: str, project: str = "default"):
        return await self._client.get(
            f"/1.0/instances/{name}/debug/repair",
            params={"project": project},
        )
