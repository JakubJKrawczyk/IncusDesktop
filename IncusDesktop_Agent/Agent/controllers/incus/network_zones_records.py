from Agent.models.emptySyncRepo_model import EmptySyncResponse
from Agent.models.network_zone_model import NetworkZoneRecordModel
from Agent.utility.rest_client import IncusRestClient


class NetworkZonesRecordsController:
    def __init__(self, client: IncusRestClient):
        self._client = client

    # GET /1.0/network-zones/{zone}/records (sync)
    async def list_records(self, zone: str, recursion: int = 0, project: str = "default") -> list[NetworkZoneRecordModel]:
        return await self._client.get(
            f"/1.0/network-zones/{zone}/records",
            params={"recursion": recursion, "project": project},
        )

    # POST /1.0/network-zones/{zone}/records (sync)
    async def create_record(self, zone: str, body: dict, project: str = "default") -> EmptySyncResponse:
        return await self._client.post(
            f"/1.0/network-zones/{zone}/records",
            json_body=body,
            params={"project": project},
        )

    # GET /1.0/network-zones/{zone}/records/{name} (sync)
    async def record_info(self, zone: str, name: str, project: str = "default") -> NetworkZoneRecordModel:
        return await self._client.get(
            f"/1.0/network-zones/{zone}/records/{name}",
            params={"project": project},
        )

    # PUT /1.0/network-zones/{zone}/records/{name} (sync)
    async def update_record(self, zone: str, name: str, body: dict, project: str = "default") -> EmptySyncResponse:
        return await self._client.put(
            f"/1.0/network-zones/{zone}/records/{name}",
            json_body=body,
            params={"project": project},
        )

    # PATCH /1.0/network-zones/{zone}/records/{name} (sync)
    async def patch_record(self, zone: str, name: str, body: dict, project: str = "default") -> EmptySyncResponse:
        return await self._client.patch(
            f"/1.0/network-zones/{zone}/records/{name}",
            json_body=body,
            params={"project": project},
        )

    # DELETE /1.0/network-zones/{zone}/records/{name} (sync)
    async def delete_record(self, zone: str, name: str, project: str = "default") -> EmptySyncResponse:
        return await self._client.delete(
            f"/1.0/network-zones/{zone}/records/{name}",
            params={"project": project},
        )
