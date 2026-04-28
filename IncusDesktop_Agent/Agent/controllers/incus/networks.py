from Agent.models.emptySyncRepo_model import EmptySyncResponse
from Agent.models.network_model import NetworkLease, NetworkModel, NetworkState
from Agent.utility.rest_client import IncusRestClient


class NetworksController:
    def __init__(self, client: IncusRestClient):
        self._client = client

    # GET /1.0/networks (sync)
    async def list_networks(
        self,
        recursion: int = 0,
        project: str = "default",
        all_projects: bool = False,
    ) -> list[NetworkModel]:
        return await self._client.get(
            "/1.0/networks",
            params={
                "recursion": recursion,
                "project": project,
                "all-projects": "true" if all_projects else None,
            },
        )

    # POST /1.0/networks (sync)
    async def create_network(self, body: dict, project: str = "default") -> EmptySyncResponse:
        return await self._client.post(
            "/1.0/networks",
            json_body=body,
            params={"project": project},
        )

    # GET /1.0/networks/{name} (sync)
    async def network_info(self, name: str, project: str = "default") -> NetworkModel:
        return await self._client.get(
            f"/1.0/networks/{name}",
            params={"project": project},
        )

    # PUT /1.0/networks/{name} (sync)
    async def update_network(self, name: str, body: dict, project: str = "default") -> EmptySyncResponse:
        return await self._client.put(
            f"/1.0/networks/{name}",
            json_body=body,
            params={"project": project},
        )

    # PATCH /1.0/networks/{name} (sync)
    async def patch_network(self, name: str, body: dict, project: str = "default") -> EmptySyncResponse:
        return await self._client.patch(
            f"/1.0/networks/{name}",
            json_body=body,
            params={"project": project},
        )

    # POST /1.0/networks/{name} (sync, rename)
    async def rename_network(self, name: str, new_name: str, project: str = "default") -> EmptySyncResponse:
        return await self._client.post(
            f"/1.0/networks/{name}",
            json_body={"name": new_name},
            params={"project": project},
        )

    # DELETE /1.0/networks/{name} (sync)
    async def delete_network(self, name: str, project: str = "default") -> EmptySyncResponse:
        return await self._client.delete(
            f"/1.0/networks/{name}",
            params={"project": project},
        )

    # GET /1.0/networks/{name}/leases (sync)
    async def network_leases(self, name: str, project: str = "default") -> list[NetworkLease]:
        return await self._client.get(
            f"/1.0/networks/{name}/leases",
            params={"project": project},
        )

    # GET /1.0/networks/{name}/state (sync)
    async def network_state(self, name: str, project: str = "default") -> NetworkState:
        return await self._client.get(
            f"/1.0/networks/{name}/state",
            params={"project": project},
        )
