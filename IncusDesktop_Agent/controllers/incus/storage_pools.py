from models.emptySyncRepo_model import EmptySyncResponse
from models.storage_model import StoragePoolModel, StoragePoolResources
from utility.rest_client import IncusRestClient


class StoragePoolsController:
    def __init__(self, client: IncusRestClient):
        self._client = client

    # GET /1.0/storage-pools (sync)
    async def list_pools(self, recursion: int = 0) -> list[StoragePoolModel]:
        return await self._client.get(
            "/1.0/storage-pools",
            params={"recursion": recursion},
        )

    # POST /1.0/storage-pools (sync)
    async def create_pool(self, body: dict) -> EmptySyncResponse:
        return await self._client.post("/1.0/storage-pools", json_body=body)

    # GET /1.0/storage-pools/{name} (sync)
    async def pool_info(self, name: str) -> StoragePoolModel:
        return await self._client.get(f"/1.0/storage-pools/{name}")

    # PUT /1.0/storage-pools/{name} (sync)
    async def update_pool(self, name: str, body: dict) -> EmptySyncResponse:
        return await self._client.put(f"/1.0/storage-pools/{name}", json_body=body)

    # PATCH /1.0/storage-pools/{name} (sync)
    async def patch_pool(self, name: str, body: dict) -> EmptySyncResponse:
        return await self._client.patch(f"/1.0/storage-pools/{name}", json_body=body)

    # DELETE /1.0/storage-pools/{name} (sync)
    async def delete_pool(self, name: str) -> EmptySyncResponse:
        return await self._client.delete(f"/1.0/storage-pools/{name}")

    # GET /1.0/storage-pools/{name}/resources (sync)
    async def pool_resources(self, name: str) -> StoragePoolResources:
        return await self._client.get(f"/1.0/storage-pools/{name}/resources")
