from Agent.models.emptySyncRepo_model import EmptySyncResponse
from Agent.models.network_model import NetworkLoadBalancer, NetworkLoadBalancerState
from Agent.utility.rest_client import IncusRestClient


class NetworksLoadBalancersController:
    def __init__(self, client: IncusRestClient):
        self._client = client

    # GET /1.0/networks/{network}/load-balancers (sync)
    async def list_load_balancers(self, network: str, recursion: int = 0, project: str = "default") -> list[NetworkLoadBalancer]:
        return await self._client.get(
            f"/1.0/networks/{network}/load-balancers",
            params={"recursion": recursion, "project": project},
        )

    # POST /1.0/networks/{network}/load-balancers (sync)
    async def create_load_balancer(self, network: str, body: dict, project: str = "default") -> EmptySyncResponse:
        return await self._client.post(
            f"/1.0/networks/{network}/load-balancers",
            json_body=body,
            params={"project": project},
        )

    # GET /1.0/networks/{network}/load-balancers/{listenAddress} (sync)
    async def load_balancer_info(self, network: str, listen_address: str, project: str = "default") -> NetworkLoadBalancer:
        return await self._client.get(
            f"/1.0/networks/{network}/load-balancers/{listen_address}",
            params={"project": project},
        )

    # PUT /1.0/networks/{network}/load-balancers/{listenAddress} (sync)
    async def update_load_balancer(self, network: str, listen_address: str, body: dict, project: str = "default") -> EmptySyncResponse:
        return await self._client.put(
            f"/1.0/networks/{network}/load-balancers/{listen_address}",
            json_body=body,
            params={"project": project},
        )

    # PATCH /1.0/networks/{network}/load-balancers/{listenAddress} (sync)
    async def patch_load_balancer(self, network: str, listen_address: str, body: dict, project: str = "default") -> EmptySyncResponse:
        return await self._client.patch(
            f"/1.0/networks/{network}/load-balancers/{listen_address}",
            json_body=body,
            params={"project": project},
        )

    # DELETE /1.0/networks/{network}/load-balancers/{listenAddress} (sync)
    async def delete_load_balancer(self, network: str, listen_address: str, project: str = "default") -> EmptySyncResponse:
        return await self._client.delete(
            f"/1.0/networks/{network}/load-balancers/{listen_address}",
            params={"project": project},
        )

    # GET /1.0/networks/{network}/load-balancers/{listenAddress}/state (sync)
    async def load_balancer_state(self, network: str, listen_address: str, project: str = "default") -> NetworkLoadBalancerState:
        return await self._client.get(
            f"/1.0/networks/{network}/load-balancers/{listen_address}/state",
            params={"project": project},
        )
