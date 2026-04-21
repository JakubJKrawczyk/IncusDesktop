from models.emptySyncRepo_model import EmptySyncResponse
from models.operation_model import OperationModel
from models.storage_model import StorageVolumeSnapshot
from utility.rest_client import IncusRestClient


class StorageVolumesSnapshotsController:
    def __init__(self, client: IncusRestClient):
        self._client = client

    # GET .../volumes/{type}/{volume}/snapshots (sync)
    async def list_snapshots(self, pool: str, type: str, volume: str, recursion: int = 0, project: str = "default") -> list[StorageVolumeSnapshot]:
        return await self._client.get(
            f"/1.0/storage-pools/{pool}/volumes/{type}/{volume}/snapshots",
            params={"recursion": recursion, "project": project},
        )

    # POST .../volumes/{type}/{volume}/snapshots (async)
    async def create_snapshot(self, pool: str, type: str, volume: str, body: dict, project: str = "default") -> OperationModel:
        return await self._client.post(
            f"/1.0/storage-pools/{pool}/volumes/{type}/{volume}/snapshots",
            json_body=body,
            params={"project": project},
        )

    # GET .../snapshots/{snapshot} (sync)
    async def snapshot_info(self, pool: str, type: str, volume: str, snapshot: str, project: str = "default") -> StorageVolumeSnapshot:
        return await self._client.get(
            f"/1.0/storage-pools/{pool}/volumes/{type}/{volume}/snapshots/{snapshot}",
            params={"project": project},
        )

    # PUT .../snapshots/{snapshot} (sync)
    async def update_snapshot(self, pool: str, type: str, volume: str, snapshot: str, body: dict, project: str = "default") -> EmptySyncResponse:
        return await self._client.put(
            f"/1.0/storage-pools/{pool}/volumes/{type}/{volume}/snapshots/{snapshot}",
            json_body=body,
            params={"project": project},
        )

    # PATCH .../snapshots/{snapshot} (sync)
    async def patch_snapshot(self, pool: str, type: str, volume: str, snapshot: str, body: dict, project: str = "default") -> EmptySyncResponse:
        return await self._client.patch(
            f"/1.0/storage-pools/{pool}/volumes/{type}/{volume}/snapshots/{snapshot}",
            json_body=body,
            params={"project": project},
        )

    # POST .../snapshots/{snapshot} (async, rename)
    async def rename_snapshot(self, pool: str, type: str, volume: str, snapshot: str, new_name: str, project: str = "default") -> OperationModel:
        return await self._client.post(
            f"/1.0/storage-pools/{pool}/volumes/{type}/{volume}/snapshots/{snapshot}",
            json_body={"name": new_name},
            params={"project": project},
        )

    # DELETE .../snapshots/{snapshot} (async)
    async def delete_snapshot(self, pool: str, type: str, volume: str, snapshot: str, project: str = "default") -> OperationModel:
        return await self._client.delete(
            f"/1.0/storage-pools/{pool}/volumes/{type}/{volume}/snapshots/{snapshot}",
            params={"project": project},
        )
