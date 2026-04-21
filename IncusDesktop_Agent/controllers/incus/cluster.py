from models.cluster_model import ClusterGroup, ClusterInfo, ClusterMember, ClusterMemberState
from models.emptySyncRepo_model import EmptySyncResponse
from models.operation_model import OperationModel
from utility.rest_client import IncusRestClient


class ClusterController:
    def __init__(self, client: IncusRestClient):
        self._client = client

    # GET /1.0/cluster (sync)
    async def cluster_info(self) -> ClusterInfo:
        return await self._client.get("/1.0/cluster")

    # PUT /1.0/cluster (async)
    async def update_cluster(self, body: dict) -> OperationModel:
        return await self._client.put("/1.0/cluster", json_body=body)

    # PUT /1.0/cluster/certificate (sync)
    async def cluster_certificate(self, body: dict) -> EmptySyncResponse:
        return await self._client.put("/1.0/cluster/certificate", json_body=body)

    # ─── Groups ────────────────────────────────────────────────────────

    # GET /1.0/cluster/groups (sync)
    async def list_groups(self, recursion: int = 0) -> list[ClusterGroup]:
        return await self._client.get("/1.0/cluster/groups", params={"recursion": recursion})

    # POST /1.0/cluster/groups (sync)
    async def create_group(self, body: dict) -> EmptySyncResponse:
        return await self._client.post("/1.0/cluster/groups", json_body=body)

    # GET /1.0/cluster/groups/{name} (sync)
    async def group_info(self, name: str) -> ClusterGroup:
        return await self._client.get(f"/1.0/cluster/groups/{name}")

    # PUT /1.0/cluster/groups/{name} (sync)
    async def update_group(self, name: str, body: dict) -> EmptySyncResponse:
        return await self._client.put(f"/1.0/cluster/groups/{name}", json_body=body)

    # PATCH /1.0/cluster/groups/{name} (sync)
    async def patch_group(self, name: str, body: dict) -> EmptySyncResponse:
        return await self._client.patch(f"/1.0/cluster/groups/{name}", json_body=body)

    # POST /1.0/cluster/groups/{name} (sync, rename)
    async def rename_group(self, name: str, new_name: str) -> EmptySyncResponse:
        return await self._client.post(
            f"/1.0/cluster/groups/{name}",
            json_body={"name": new_name},
        )

    # DELETE /1.0/cluster/groups/{name} (sync)
    async def delete_group(self, name: str) -> EmptySyncResponse:
        return await self._client.delete(f"/1.0/cluster/groups/{name}")

    # ─── Members ───────────────────────────────────────────────────────

    # GET /1.0/cluster/members (sync)
    async def list_members(self, recursion: int = 0) -> list[ClusterMember]:
        return await self._client.get("/1.0/cluster/members", params={"recursion": recursion})

    # POST /1.0/cluster/members (async, request join token)
    async def request_join_token(self, body: dict) -> OperationModel:
        return await self._client.post("/1.0/cluster/members", json_body=body)

    # GET /1.0/cluster/members/{name} (sync)
    async def member_info(self, name: str) -> ClusterMember:
        return await self._client.get(f"/1.0/cluster/members/{name}")

    # PUT /1.0/cluster/members/{name} (sync)
    async def update_member(self, name: str, body: dict) -> EmptySyncResponse:
        return await self._client.put(f"/1.0/cluster/members/{name}", json_body=body)

    # PATCH /1.0/cluster/members/{name} (sync)
    async def patch_member(self, name: str, body: dict) -> EmptySyncResponse:
        return await self._client.patch(f"/1.0/cluster/members/{name}", json_body=body)

    # POST /1.0/cluster/members/{name} (sync, rename)
    async def rename_member(self, name: str, new_name: str) -> EmptySyncResponse:
        return await self._client.post(
            f"/1.0/cluster/members/{name}",
            json_body={"name": new_name},
        )

    # DELETE /1.0/cluster/members/{name} (sync)
    async def delete_member(self, name: str, force: bool = False) -> EmptySyncResponse:
        return await self._client.delete(
            f"/1.0/cluster/members/{name}",
            params={"force": "1" if force else None},
        )

    # GET /1.0/cluster/members/{name}/state (sync)
    async def member_state(self, name: str) -> ClusterMemberState:
        return await self._client.get(f"/1.0/cluster/members/{name}/state")

    # POST /1.0/cluster/members/{name}/state (async)
    async def member_state_action(self, name: str, body: dict) -> OperationModel:
        return await self._client.post(f"/1.0/cluster/members/{name}/state", json_body=body)
