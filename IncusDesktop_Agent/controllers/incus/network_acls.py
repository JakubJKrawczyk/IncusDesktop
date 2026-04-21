from models.emptySyncRepo_model import EmptySyncResponse
from models.network_acl_model import NetworkACLModel
from utility.rest_client import IncusRestClient


class NetworkACLsController:
    def __init__(self, client: IncusRestClient):
        self._client = client

    # GET /1.0/network-acls (sync)
    async def list_acls(self, recursion: int = 0, project: str = "default") -> list[NetworkACLModel]:
        return await self._client.get(
            "/1.0/network-acls",
            params={"recursion": recursion, "project": project},
        )

    # POST /1.0/network-acls (sync)
    async def create_acl(self, body: dict, project: str = "default") -> EmptySyncResponse:
        return await self._client.post(
            "/1.0/network-acls",
            json_body=body,
            params={"project": project},
        )

    # GET /1.0/network-acls/{name} (sync)
    async def acl_info(self, name: str, project: str = "default") -> NetworkACLModel:
        return await self._client.get(
            f"/1.0/network-acls/{name}",
            params={"project": project},
        )

    # PUT /1.0/network-acls/{name} (sync)
    async def update_acl(self, name: str, body: dict, project: str = "default") -> EmptySyncResponse:
        return await self._client.put(
            f"/1.0/network-acls/{name}",
            json_body=body,
            params={"project": project},
        )

    # PATCH /1.0/network-acls/{name} (sync)
    async def patch_acl(self, name: str, body: dict, project: str = "default") -> EmptySyncResponse:
        return await self._client.patch(
            f"/1.0/network-acls/{name}",
            json_body=body,
            params={"project": project},
        )

    # POST /1.0/network-acls/{name} (sync, rename)
    async def rename_acl(self, name: str, new_name: str, project: str = "default") -> EmptySyncResponse:
        return await self._client.post(
            f"/1.0/network-acls/{name}",
            json_body={"name": new_name},
            params={"project": project},
        )

    # DELETE /1.0/network-acls/{name} (sync)
    async def delete_acl(self, name: str, project: str = "default") -> EmptySyncResponse:
        return await self._client.delete(
            f"/1.0/network-acls/{name}",
            params={"project": project},
        )

    # GET /1.0/network-acls/{name}/log (raw text)
    async def acl_log(self, name: str, project: str = "default") -> bytes:
        return await self._client.get(
            f"/1.0/network-acls/{name}/log",
            params={"project": project},
            raw=True,
        )
