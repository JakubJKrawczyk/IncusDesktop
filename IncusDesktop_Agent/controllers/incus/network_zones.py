from models.emptySyncRepo_model import EmptySyncResponse
from models.network_zone_model import NetworkZoneModel
from utility.rest_client import IncusRestClient


class NetworkZonesController:
    def __init__(self, client: IncusRestClient):
        self._client = client

    # GET /1.0/network-zones (sync)
    async def list_zones(self, recursion: int = 0, project: str = "default") -> list[NetworkZoneModel]:
        return await self._client.get(
            "/1.0/network-zones",
            params={"recursion": recursion, "project": project},
        )

    # POST /1.0/network-zones (sync)
    async def create_zone(self, body: dict, project: str = "default") -> EmptySyncResponse:
        return await self._client.post(
            "/1.0/network-zones",
            json_body=body,
            params={"project": project},
        )

    # GET /1.0/network-zones/{name} (sync)
    async def zone_info(self, name: str, project: str = "default") -> NetworkZoneModel:
        return await self._client.get(
            f"/1.0/network-zones/{name}",
            params={"project": project},
        )

    # PUT /1.0/network-zones/{name} (sync)
    async def update_zone(self, name: str, body: dict, project: str = "default") -> EmptySyncResponse:
        return await self._client.put(
            f"/1.0/network-zones/{name}",
            json_body=body,
            params={"project": project},
        )

    # PATCH /1.0/network-zones/{name} (sync)
    async def patch_zone(self, name: str, body: dict, project: str = "default") -> EmptySyncResponse:
        return await self._client.patch(
            f"/1.0/network-zones/{name}",
            json_body=body,
            params={"project": project},
        )

    # DELETE /1.0/network-zones/{name} (sync)
    async def delete_zone(self, name: str, project: str = "default") -> EmptySyncResponse:
        return await self._client.delete(
            f"/1.0/network-zones/{name}",
            params={"project": project},
        )
