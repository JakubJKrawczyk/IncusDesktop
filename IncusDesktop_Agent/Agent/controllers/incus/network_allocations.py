from Agent.models.network_allocation_model import NetworkAllocationModel
from Agent.utility.rest_client import IncusRestClient


class NetworkAllocationsController:
    def __init__(self, client: IncusRestClient):
        self._client = client

    # GET /1.0/network-allocations (sync)
    async def list_allocations(self, project: str = "default", all_projects: bool = False) -> list[NetworkAllocationModel]:
        return await self._client.get(
            "/1.0/network-allocations",
            params={
                "project": project,
                "all-projects": "true" if all_projects else None,
            },
        )
