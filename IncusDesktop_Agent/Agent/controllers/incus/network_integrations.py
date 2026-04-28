from Agent.models.emptySyncRepo_model import EmptySyncResponse
from Agent.models.network_integration_model import NetworkIntegrationModel
from Agent.utility.rest_client import IncusRestClient


class NetworkIntegrationsController:
    def __init__(self, client: IncusRestClient):
        self._client = client

    # GET /1.0/network-integrations (sync)
    async def list_integrations(self, recursion: int = 0) -> list[NetworkIntegrationModel]:
        return await self._client.get(
            "/1.0/network-integrations",
            params={"recursion": recursion},
        )

    # POST /1.0/network-integrations (sync)
    async def create_integration(self, body: dict) -> EmptySyncResponse:
        return await self._client.post("/1.0/network-integrations", json_body=body)

    # GET /1.0/network-integrations/{name} (sync)
    async def integration_info(self, name: str) -> NetworkIntegrationModel:
        return await self._client.get(f"/1.0/network-integrations/{name}")

    # PUT /1.0/network-integrations/{name} (sync)
    async def update_integration(self, name: str, body: dict) -> EmptySyncResponse:
        return await self._client.put(f"/1.0/network-integrations/{name}", json_body=body)

    # PATCH /1.0/network-integrations/{name} (sync)
    async def patch_integration(self, name: str, body: dict) -> EmptySyncResponse:
        return await self._client.patch(f"/1.0/network-integrations/{name}", json_body=body)

    # POST /1.0/network-integrations/{name} (sync, rename)
    async def rename_integration(self, name: str, new_name: str) -> EmptySyncResponse:
        return await self._client.post(
            f"/1.0/network-integrations/{name}",
            json_body={"name": new_name},
        )

    # DELETE /1.0/network-integrations/{name} (sync)
    async def delete_integration(self, name: str) -> EmptySyncResponse:
        return await self._client.delete(f"/1.0/network-integrations/{name}")
