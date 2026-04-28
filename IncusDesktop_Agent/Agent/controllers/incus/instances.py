from Agent.models.emptySyncRepo_model import EmptySyncResponse
from Agent.models.instance_model import InstanceModel, InstanceState
from Agent.models.operation_model import OperationModel
from Agent.utility.rest_client import IncusRestClient
from Agent.models.access_model import Access


class InstancesController:
    def __init__(self, client: IncusRestClient):
        self._client = client

    # GET /1.0/instances (sync)
    async def list_instances(self, project: str = "default", filter: str | None = None) -> list[InstanceModel]:
        return await self._client.get(
            "/1.0/instances",
            params={"recursion": 1, "project": project, "filter": filter},
        )

    # POST /1.0/instances (async)
    async def create_instance(self, body: dict, project: str = "default") -> OperationModel:
        return await self._client.post(
            "/1.0/instances",
            json_body=body,
            params={"project": project},
        )

    # PUT /1.0/instances (async)
    async def bulk_update_instances(self, body: dict, project: str = "default") -> OperationModel:
        return await self._client.put(
            "/1.0/instances",
            json_body=body,
            params={"project": project},
        )

    # GET /1.0/instances/{name} (sync)
    async def instance_info(self, name: str, project: str = "default") -> InstanceModel:
        return await self._client.get(
            f"/1.0/instances/{name}",
            params={"recursion": 1, "project": project},
        )

    # PUT /1.0/instances/{name} (async)
    async def update_instance(self, name: str, body: dict, project: str = "default") -> OperationModel:
        return await self._client.put(
            f"/1.0/instances/{name}",
            json_body=body,
            params={"project": project},
        )

    # PATCH /1.0/instances/{name} (sync)
    async def patch_instance(self, name: str, body: dict, project: str = "default") -> EmptySyncResponse:
        return await self._client.patch(
            f"/1.0/instances/{name}",
            json_body=body,
            params={"project": project},
        )

    # POST /1.0/instances/{name} (async)
    async def rename_instance(self, name: str, new_name: str, project: str = "default") -> OperationModel:
        return await self._client.post(
            f"/1.0/instances/{name}",
            json_body={"name": new_name},
            params={"project": project},
        )

    # DELETE /1.0/instances/{name} (async)
    async def delete_instance(self, name: str, project: str = "default") -> OperationModel:
        return await self._client.delete(
            f"/1.0/instances/{name}",
            params={"project": project},
        )

    # GET /1.0/instances/{name}/access (sync)
    async def instance_access(self, name: str, project: str = "default") -> Access:
        return await self._client.get(
            f"/1.0/instances/{name}/access",
            params={"project": project},
        )

    # GET /1.0/instances/{name}/state (sync)
    async def instance_state(self, name: str, project: str = "default") -> InstanceState:
        return await self._client.get(
            f"/1.0/instances/{name}/state",
            params={"project": project},
        )

    # PUT /1.0/instances/{name}/state (async)
    async def set_instance_state(
        self,
        name: str,
        action: str,
        timeout: int = 30,
        force: bool = False,
        stateful: bool = False,
        project: str = "default",
    ) -> OperationModel:
        return await self._client.put(
            f"/1.0/instances/{name}/state",
            json_body={
                "action": action,
                "timeout": timeout,
                "force": force,
                "stateful": stateful,
            },
            params={"project": project},
        )

    # POST /1.0/instances/{name}/rebuild (async)
    async def rebuild_instance(self, name: str, source: dict, project: str = "default") -> OperationModel:
        return await self._client.post(
            f"/1.0/instances/{name}/rebuild",
            json_body={"source": source},
            params={"project": project},
        )
