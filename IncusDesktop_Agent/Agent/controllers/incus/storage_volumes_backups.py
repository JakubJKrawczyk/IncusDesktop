from Agent.models.operation_model import OperationModel
from Agent.models.storage_model import StorageVolumeBackup
from Agent.utility.rest_client import IncusRestClient


class StorageVolumesBackupsController:
    def __init__(self, client: IncusRestClient):
        self._client = client

    # GET .../volumes/{type}/{volume}/backups (sync)
    async def list_backups(self, pool: str, type: str, volume: str, recursion: int = 0, project: str = "default") -> list[StorageVolumeBackup]:
        return await self._client.get(
            f"/1.0/storage-pools/{pool}/volumes/{type}/{volume}/backups",
            params={"recursion": recursion, "project": project},
        )

    # POST .../volumes/{type}/{volume}/backups (async)
    async def create_backup(self, pool: str, type: str, volume: str, body: dict, project: str = "default") -> OperationModel:
        return await self._client.post(
            f"/1.0/storage-pools/{pool}/volumes/{type}/{volume}/backups",
            json_body=body,
            params={"project": project},
        )

    # GET .../backups/{backup} (sync)
    async def backup_info(self, pool: str, type: str, volume: str, backup: str, project: str = "default") -> StorageVolumeBackup:
        return await self._client.get(
            f"/1.0/storage-pools/{pool}/volumes/{type}/{volume}/backups/{backup}",
            params={"project": project},
        )

    # POST .../backups/{backup} (async, rename)
    async def rename_backup(self, pool: str, type: str, volume: str, backup: str, new_name: str, project: str = "default") -> OperationModel:
        return await self._client.post(
            f"/1.0/storage-pools/{pool}/volumes/{type}/{volume}/backups/{backup}",
            json_body={"name": new_name},
            params={"project": project},
        )

    # DELETE .../backups/{backup} (async)
    async def delete_backup(self, pool: str, type: str, volume: str, backup: str, project: str = "default") -> OperationModel:
        return await self._client.delete(
            f"/1.0/storage-pools/{pool}/volumes/{type}/{volume}/backups/{backup}",
            params={"project": project},
        )

    # GET .../backups/{backup}/export (raw)
    async def export_backup(self, pool: str, type: str, volume: str, backup: str, project: str = "default") -> bytes:
        return await self._client.get(
            f"/1.0/storage-pools/{pool}/volumes/{type}/{volume}/backups/{backup}/export",
            params={"project": project},
            raw=True,
        )
