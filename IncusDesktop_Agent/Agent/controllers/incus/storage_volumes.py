from Agent.models.emptySyncRepo_model import EmptySyncResponse
from Agent.models.operation_model import OperationModel
from Agent.models.storage_model import StorageVolumeModel, StorageVolumeState
from Agent.utility.rest_client import IncusRestClient


class StorageVolumesController:
    def __init__(self, client: IncusRestClient):
        self._client = client

    # GET /1.0/storage-pools/{pool}/volumes (sync, without type filter)
    async def list_volumes(self, pool: str, recursion: int = 0, project: str = "default") -> list[StorageVolumeModel]:
        return await self._client.get(
            f"/1.0/storage-pools/{pool}/volumes",
            params={"recursion": recursion, "project": project},
        )

    # GET /1.0/storage-pools/{pool}/volumes/{type} (sync, filtered)
    async def list_volumes_by_type(self, pool: str, type: str, recursion: int = 0, project: str = "default") -> list[StorageVolumeModel]:
        return await self._client.get(
            f"/1.0/storage-pools/{pool}/volumes/{type}",
            params={"recursion": recursion, "project": project},
        )

    # POST /1.0/storage-pools/{pool}/volumes (sync, JSON create)
    async def create_volume(self, pool: str, body: dict, project: str = "default") -> EmptySyncResponse:
        return await self._client.post(
            f"/1.0/storage-pools/{pool}/volumes",
            json_body=body,
            params={"project": project},
        )

    # POST /1.0/storage-pools/{pool}/volumes/{type} (sync, typed create)
    async def create_volume_by_type(self, pool: str, type: str, body: dict, project: str = "default") -> EmptySyncResponse:
        return await self._client.post(
            f"/1.0/storage-pools/{pool}/volumes/{type}",
            json_body=body,
            params={"project": project},
        )

    # POST /1.0/storage-pools/{pool}/volumes/custom (import backup, raw, async)
    async def import_volume_from_backup(
        self,
        pool: str,
        content: bytes,
        headers: dict | None = None,
        project: str = "default",
    ) -> OperationModel:
        return await self._client.post_raw(
            f"/1.0/storage-pools/{pool}/volumes/custom",
            content=content,
            params={"project": project},
            headers=headers,
        )

    # GET /1.0/storage-pools/{pool}/volumes/{type}/{name} (sync)
    async def volume_info(self, pool: str, type: str, name: str, project: str = "default") -> StorageVolumeModel:
        return await self._client.get(
            f"/1.0/storage-pools/{pool}/volumes/{type}/{name}",
            params={"project": project},
        )

    # PUT /1.0/storage-pools/{pool}/volumes/{type}/{name} (sync)
    async def update_volume(self, pool: str, type: str, name: str, body: dict, project: str = "default") -> EmptySyncResponse:
        return await self._client.put(
            f"/1.0/storage-pools/{pool}/volumes/{type}/{name}",
            json_body=body,
            params={"project": project},
        )

    # PATCH /1.0/storage-pools/{pool}/volumes/{type}/{name} (sync)
    async def patch_volume(self, pool: str, type: str, name: str, body: dict, project: str = "default") -> EmptySyncResponse:
        return await self._client.patch(
            f"/1.0/storage-pools/{pool}/volumes/{type}/{name}",
            json_body=body,
            params={"project": project},
        )

    # POST /1.0/storage-pools/{pool}/volumes/{type}/{name} (async, rename/migrate)
    async def rename_volume(self, pool: str, type: str, name: str, body: dict, project: str = "default") -> OperationModel:
        return await self._client.post(
            f"/1.0/storage-pools/{pool}/volumes/{type}/{name}",
            json_body=body,
            params={"project": project},
        )

    # DELETE /1.0/storage-pools/{pool}/volumes/{type}/{name} (sync)
    async def delete_volume(self, pool: str, type: str, name: str, project: str = "default") -> EmptySyncResponse:
        return await self._client.delete(
            f"/1.0/storage-pools/{pool}/volumes/{type}/{name}",
            params={"project": project},
        )

    # GET /1.0/storage-pools/{pool}/volumes/{type}/{name}/state (sync)
    async def volume_state(self, pool: str, type: str, name: str, project: str = "default") -> StorageVolumeState:
        return await self._client.get(
            f"/1.0/storage-pools/{pool}/volumes/{type}/{name}/state",
            params={"project": project},
        )

    # GET /1.0/storage-pools/{pool}/volumes/{type}/{name}/nbd (placeholder 501)
    async def volume_nbd(self, pool: str, type: str, name: str, project: str = "default"):
        raise NotImplementedError("NBD endpoint requires socket hijacking")

    # GET /1.0/storage-pools/{pool}/volumes/{type}/{name}/sftp (placeholder 501)
    async def volume_sftp(self, pool: str, type: str, name: str, project: str = "default"):
        raise NotImplementedError("SFTP endpoint requires HTTP upgrade")
