from models.emptySyncRepo_model import EmptySyncResponse
from models.network_model import NetworkPeer
from utility.rest_client import IncusRestClient


class NetworksPeersController:
    def __init__(self, client: IncusRestClient):
        self._client = client

    # GET /1.0/networks/{network}/peers (sync)
    async def list_peers(self, network: str, recursion: int = 0, project: str = "default") -> list[NetworkPeer]:
        return await self._client.get(
            f"/1.0/networks/{network}/peers",
            params={"recursion": recursion, "project": project},
        )

    # POST /1.0/networks/{network}/peers (sync)
    async def create_peer(self, network: str, body: dict, project: str = "default") -> EmptySyncResponse:
        return await self._client.post(
            f"/1.0/networks/{network}/peers",
            json_body=body,
            params={"project": project},
        )

    # GET /1.0/networks/{network}/peers/{peerName} (sync)
    async def peer_info(self, network: str, peer_name: str, project: str = "default") -> NetworkPeer:
        return await self._client.get(
            f"/1.0/networks/{network}/peers/{peer_name}",
            params={"project": project},
        )

    # PUT /1.0/networks/{network}/peers/{peerName} (sync)
    async def update_peer(self, network: str, peer_name: str, body: dict, project: str = "default") -> EmptySyncResponse:
        return await self._client.put(
            f"/1.0/networks/{network}/peers/{peer_name}",
            json_body=body,
            params={"project": project},
        )

    # PATCH /1.0/networks/{network}/peers/{peerName} (sync)
    async def patch_peer(self, network: str, peer_name: str, body: dict, project: str = "default") -> EmptySyncResponse:
        return await self._client.patch(
            f"/1.0/networks/{network}/peers/{peer_name}",
            json_body=body,
            params={"project": project},
        )

    # DELETE /1.0/networks/{network}/peers/{peerName} (sync)
    async def delete_peer(self, network: str, peer_name: str, project: str = "default") -> EmptySyncResponse:
        return await self._client.delete(
            f"/1.0/networks/{network}/peers/{peer_name}",
            params={"project": project},
        )
