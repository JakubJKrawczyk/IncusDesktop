from Agent.models.emptySyncRepo_model import EmptySyncResponse
from Agent.models.storage_model import StorageBucketModel
from Agent.utility.rest_client import IncusRestClient


class StorageBucketsController:
    def __init__(self, client: IncusRestClient):
        self._client = client

    # GET /1.0/storage-pools/{pool}/buckets (sync)
    async def list_buckets(self, pool: str, recursion: int = 0, project: str = "default") -> list[StorageBucketModel]:
        return await self._client.get(
            f"/1.0/storage-pools/{pool}/buckets",
            params={"recursion": recursion, "project": project},
        )

    # POST /1.0/storage-pools/{pool}/buckets (sync)
    async def create_bucket(self, pool: str, body: dict, project: str = "default") -> EmptySyncResponse:
        return await self._client.post(
            f"/1.0/storage-pools/{pool}/buckets",
            json_body=body,
            params={"project": project},
        )

    # GET /1.0/storage-pools/{pool}/buckets/{name} (sync)
    async def bucket_info(self, pool: str, name: str, project: str = "default") -> StorageBucketModel:
        return await self._client.get(
            f"/1.0/storage-pools/{pool}/buckets/{name}",
            params={"project": project},
        )

    # PUT /1.0/storage-pools/{pool}/buckets/{name} (sync)
    async def update_bucket(self, pool: str, name: str, body: dict, project: str = "default") -> EmptySyncResponse:
        return await self._client.put(
            f"/1.0/storage-pools/{pool}/buckets/{name}",
            json_body=body,
            params={"project": project},
        )

    # PATCH /1.0/storage-pools/{pool}/buckets/{name} (sync)
    async def patch_bucket(self, pool: str, name: str, body: dict, project: str = "default") -> EmptySyncResponse:
        return await self._client.patch(
            f"/1.0/storage-pools/{pool}/buckets/{name}",
            json_body=body,
            params={"project": project},
        )

    # DELETE /1.0/storage-pools/{pool}/buckets/{name} (sync)
    async def delete_bucket(self, pool: str, name: str, project: str = "default") -> EmptySyncResponse:
        return await self._client.delete(
            f"/1.0/storage-pools/{pool}/buckets/{name}",
            params={"project": project},
        )
