from models.instance_model import InstanceBackup
from models.operation_model import OperationModel
from utility.rest_client import IncusRestClient


class InstancesBackupsController:
    def __init__(self, client: IncusRestClient):
        self._client = client

    # GET /1.0/instances/{name}/backups (sync)
    async def list_backups(self, name: str, recursion: int = 0, project: str = "default") -> list[InstanceBackup]:
        return await self._client.get(
            f"/1.0/instances/{name}/backups",
            params={"recursion": recursion, "project": project},
        )

    # POST /1.0/instances/{name}/backups (async)
    async def create_backup(self, name: str, body: dict, project: str = "default") -> OperationModel:
        return await self._client.post(
            f"/1.0/instances/{name}/backups",
            json_body=body,
            params={"project": project},
        )

    # GET /1.0/instances/{name}/backups/{backup} (sync)
    async def backup_info(self, name: str, backup: str, project: str = "default") -> InstanceBackup:
        return await self._client.get(
            f"/1.0/instances/{name}/backups/{backup}",
            params={"project": project},
        )

    # POST /1.0/instances/{name}/backups/{backup} (async)
    async def rename_backup(self, name: str, backup: str, new_name: str, project: str = "default") -> OperationModel:
        return await self._client.post(
            f"/1.0/instances/{name}/backups/{backup}",
            json_body={"name": new_name},
            params={"project": project},
        )

    # DELETE /1.0/instances/{name}/backups/{backup} (async)
    async def delete_backup(self, name: str, backup: str, project: str = "default") -> OperationModel:
        return await self._client.delete(
            f"/1.0/instances/{name}/backups/{backup}",
            params={"project": project},
        )

    # GET /1.0/instances/{name}/backups/{backup}/export (raw)
    async def export_backup(self, name: str, backup: str, project: str = "default") -> bytes:
        return await self._client.get(
            f"/1.0/instances/{name}/backups/{backup}/export",
            params={"project": project},
            raw=True,
        )
