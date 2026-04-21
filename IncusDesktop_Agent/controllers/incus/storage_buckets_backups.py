from models.operation_model import OperationModel
from models.storage_model import StorageBucketBackup
from utility.rest_client import IncusRestClient


class StorageBucketsBackupsController:
    def __init__(self, client: IncusRestClient):
        self._client = client

    # GET .../buckets/{bucket}/backups (sync)
    async def list_backups(self, pool: str, bucket: str, recursion: int = 0, project: str = "default") -> list[StorageBucketBackup]:
        return await self._client.get(
            f"/1.0/storage-pools/{pool}/buckets/{bucket}/backups",
            params={"recursion": recursion, "project": project},
        )

    # POST .../buckets/{bucket}/backups (async)
    async def create_backup(self, pool: str, bucket: str, body: dict, project: str = "default") -> OperationModel:
        return await self._client.post(
            f"/1.0/storage-pools/{pool}/buckets/{bucket}/backups",
            json_body=body,
            params={"project": project},
        )

    # GET .../backups/{backup} (sync)
    async def backup_info(self, pool: str, bucket: str, backup: str, project: str = "default") -> StorageBucketBackup:
        return await self._client.get(
            f"/1.0/storage-pools/{pool}/buckets/{bucket}/backups/{backup}",
            params={"project": project},
        )

    # POST .../backups/{backup} (async, rename)
    async def rename_backup(self, pool: str, bucket: str, backup: str, new_name: str, project: str = "default") -> OperationModel:
        return await self._client.post(
            f"/1.0/storage-pools/{pool}/buckets/{bucket}/backups/{backup}",
            json_body={"name": new_name},
            params={"project": project},
        )

    # DELETE .../backups/{backup} (async)
    async def delete_backup(self, pool: str, bucket: str, backup: str, project: str = "default") -> OperationModel:
        return await self._client.delete(
            f"/1.0/storage-pools/{pool}/buckets/{bucket}/backups/{backup}",
            params={"project": project},
        )

    # GET .../backups/{backup}/export (raw)
    async def export_backup(self, pool: str, bucket: str, backup: str, project: str = "default") -> bytes:
        return await self._client.get(
            f"/1.0/storage-pools/{pool}/buckets/{bucket}/backups/{backup}/export",
            params={"project": project},
            raw=True,
        )
