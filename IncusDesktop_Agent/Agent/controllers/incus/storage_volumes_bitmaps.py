from Agent.models.operation_model import OperationModel
from Agent.models.storage_model import StorageVolumeBitmap
from Agent.utility.rest_client import IncusRestClient


class StorageVolumesBitmapsController:
    def __init__(self, client: IncusRestClient):
        self._client = client

    # GET .../volumes/{type}/{volume}/bitmaps (sync)
    async def list_bitmaps(self, pool: str, type: str, volume: str, recursion: int = 0, project: str = "default") -> list[StorageVolumeBitmap]:
        return await self._client.get(
            f"/1.0/storage-pools/{pool}/volumes/{type}/{volume}/bitmaps",
            params={"recursion": recursion, "project": project},
        )

    # POST .../volumes/{type}/{volume}/bitmaps (async)
    async def create_bitmap(self, pool: str, type: str, volume: str, body: dict, project: str = "default") -> OperationModel:
        return await self._client.post(
            f"/1.0/storage-pools/{pool}/volumes/{type}/{volume}/bitmaps",
            json_body=body,
            params={"project": project},
        )

    # DELETE .../bitmaps/{bitmap} (async)
    async def delete_bitmap(self, pool: str, type: str, volume: str, bitmap: str, project: str = "default") -> OperationModel:
        return await self._client.delete(
            f"/1.0/storage-pools/{pool}/volumes/{type}/{volume}/bitmaps/{bitmap}",
            params={"project": project},
        )
