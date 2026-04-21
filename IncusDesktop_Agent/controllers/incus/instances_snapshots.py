from models.emptySyncRepo_model import EmptySyncResponse
from models.instance_model import InstanceSnapshot
from models.operation_model import OperationModel
from utility.rest_client import IncusRestClient


class InstancesSnapshotsController:
    def __init__(self, client: IncusRestClient):
        self._client = client

    # GET /1.0/instances/{name}/snapshots (sync)
    async def list_snapshots(self, name: str, recursion: int = 0, project: str = "default") -> list[InstanceSnapshot]:
        return await self._client.get(
            f"/1.0/instances/{name}/snapshots",
            params={"recursion": recursion, "project": project},
        )

    # POST /1.0/instances/{name}/snapshots (async)
    async def create_snapshot(self, name: str, body: dict, project: str = "default") -> OperationModel:
        return await self._client.post(
            f"/1.0/instances/{name}/snapshots",
            json_body=body,
            params={"project": project},
        )

    # GET /1.0/instances/{name}/snapshots/{snapshot} (sync)
    async def snapshot_info(self, name: str, snapshot: str, project: str = "default") -> InstanceSnapshot:
        return await self._client.get(
            f"/1.0/instances/{name}/snapshots/{snapshot}",
            params={"project": project},
        )

    # PUT /1.0/instances/{name}/snapshots/{snapshot} (async)
    async def update_snapshot(self, name: str, snapshot: str, body: dict, project: str = "default") -> OperationModel:
        return await self._client.put(
            f"/1.0/instances/{name}/snapshots/{snapshot}",
            json_body=body,
            params={"project": project},
        )

    # PATCH /1.0/instances/{name}/snapshots/{snapshot} (sync)
    async def patch_snapshot(self, name: str, snapshot: str, body: dict, project: str = "default") -> EmptySyncResponse:
        return await self._client.patch(
            f"/1.0/instances/{name}/snapshots/{snapshot}",
            json_body=body,
            params={"project": project},
        )

    # POST /1.0/instances/{name}/snapshots/{snapshot} (async)
    async def rename_snapshot(self, name: str, snapshot: str, new_name: str, project: str = "default") -> OperationModel:
        return await self._client.post(
            f"/1.0/instances/{name}/snapshots/{snapshot}",
            json_body={"name": new_name},
            params={"project": project},
        )

    # DELETE /1.0/instances/{name}/snapshots/{snapshot} (async)
    async def delete_snapshot(self, name: str, snapshot: str, project: str = "default") -> OperationModel:
        return await self._client.delete(
            f"/1.0/instances/{name}/snapshots/{snapshot}",
            params={"project": project},
        )
