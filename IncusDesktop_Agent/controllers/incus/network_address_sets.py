from models.emptySyncRepo_model import EmptySyncResponse
from models.network_address_set_model import NetworkAddressSetModel
from utility.rest_client import IncusRestClient


class NetworkAddressSetsController:
    def __init__(self, client: IncusRestClient):
        self._client = client

    # GET /1.0/network-address-sets (sync)
    async def list_address_sets(self, recursion: int = 0, project: str = "default") -> list[NetworkAddressSetModel]:
        return await self._client.get(
            "/1.0/network-address-sets",
            params={"recursion": recursion, "project": project},
        )

    # POST /1.0/network-address-sets (sync)
    async def create_address_set(self, body: dict, project: str = "default") -> EmptySyncResponse:
        return await self._client.post(
            "/1.0/network-address-sets",
            json_body=body,
            params={"project": project},
        )

    # GET /1.0/network-address-sets/{name} (sync)
    async def address_set_info(self, name: str, project: str = "default") -> NetworkAddressSetModel:
        return await self._client.get(
            f"/1.0/network-address-sets/{name}",
            params={"project": project},
        )

    # PUT /1.0/network-address-sets/{name} (sync)
    async def update_address_set(self, name: str, body: dict, project: str = "default") -> EmptySyncResponse:
        return await self._client.put(
            f"/1.0/network-address-sets/{name}",
            json_body=body,
            params={"project": project},
        )

    # PATCH /1.0/network-address-sets/{name} (sync)
    async def patch_address_set(self, name: str, body: dict, project: str = "default") -> EmptySyncResponse:
        return await self._client.patch(
            f"/1.0/network-address-sets/{name}",
            json_body=body,
            params={"project": project},
        )

    # POST /1.0/network-address-sets/{name} (sync, rename)
    async def rename_address_set(self, name: str, new_name: str, project: str = "default") -> EmptySyncResponse:
        return await self._client.post(
            f"/1.0/network-address-sets/{name}",
            json_body={"name": new_name},
            params={"project": project},
        )

    # DELETE /1.0/network-address-sets/{name} (sync)
    async def delete_address_set(self, name: str, project: str = "default") -> EmptySyncResponse:
        return await self._client.delete(
            f"/1.0/network-address-sets/{name}",
            params={"project": project},
        )
