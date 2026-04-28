from Agent.models.emptySyncRepo_model import EmptySyncResponse
from Agent.models.network_model import NetworkForward
from Agent.utility.rest_client import IncusRestClient


class NetworksForwardsController:
    def __init__(self, client: IncusRestClient):
        self._client = client

    # GET /1.0/networks/{network}/forwards (sync)
    async def list_forwards(self, network: str, recursion: int = 0, project: str = "default") -> list[NetworkForward]:
        return await self._client.get(
            f"/1.0/networks/{network}/forwards",
            params={"recursion": recursion, "project": project},
        )

    # POST /1.0/networks/{network}/forwards (sync)
    async def create_forward(self, network: str, body: dict, project: str = "default") -> EmptySyncResponse:
        return await self._client.post(
            f"/1.0/networks/{network}/forwards",
            json_body=body,
            params={"project": project},
        )

    # GET /1.0/networks/{network}/forwards/{listenAddress} (sync)
    async def forward_info(self, network: str, listen_address: str, project: str = "default") -> NetworkForward:
        return await self._client.get(
            f"/1.0/networks/{network}/forwards/{listen_address}",
            params={"project": project},
        )

    # PUT /1.0/networks/{network}/forwards/{listenAddress} (sync)
    async def update_forward(self, network: str, listen_address: str, body: dict, project: str = "default") -> EmptySyncResponse:
        return await self._client.put(
            f"/1.0/networks/{network}/forwards/{listen_address}",
            json_body=body,
            params={"project": project},
        )

    # PATCH /1.0/networks/{network}/forwards/{listenAddress} (sync)
    async def patch_forward(self, network: str, listen_address: str, body: dict, project: str = "default") -> EmptySyncResponse:
        return await self._client.patch(
            f"/1.0/networks/{network}/forwards/{listen_address}",
            json_body=body,
            params={"project": project},
        )

    # DELETE /1.0/networks/{network}/forwards/{listenAddress} (sync)
    async def delete_forward(self, network: str, listen_address: str, project: str = "default") -> EmptySyncResponse:
        return await self._client.delete(
            f"/1.0/networks/{network}/forwards/{listen_address}",
            params={"project": project},
        )
