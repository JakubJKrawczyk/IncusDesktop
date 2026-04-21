from models.emptySyncRepo_model import EmptySyncResponse
from models.storage_model import StorageBucketKey
from utility.rest_client import IncusRestClient


class StorageBucketsKeysController:
    def __init__(self, client: IncusRestClient):
        self._client = client

    # GET .../buckets/{bucket}/keys (sync)
    async def list_keys(self, pool: str, bucket: str, recursion: int = 0, project: str = "default") -> list[StorageBucketKey]:
        return await self._client.get(
            f"/1.0/storage-pools/{pool}/buckets/{bucket}/keys",
            params={"recursion": recursion, "project": project},
        )

    # POST .../buckets/{bucket}/keys (sync)
    async def create_key(self, pool: str, bucket: str, body: dict, project: str = "default") -> EmptySyncResponse:
        return await self._client.post(
            f"/1.0/storage-pools/{pool}/buckets/{bucket}/keys",
            json_body=body,
            params={"project": project},
        )

    # GET .../keys/{key} (sync)
    async def key_info(self, pool: str, bucket: str, key: str, project: str = "default") -> StorageBucketKey:
        return await self._client.get(
            f"/1.0/storage-pools/{pool}/buckets/{bucket}/keys/{key}",
            params={"project": project},
        )

    # PUT .../keys/{key} (sync)
    async def update_key(self, pool: str, bucket: str, key: str, body: dict, project: str = "default") -> EmptySyncResponse:
        return await self._client.put(
            f"/1.0/storage-pools/{pool}/buckets/{bucket}/keys/{key}",
            json_body=body,
            params={"project": project},
        )

    # PATCH .../keys/{key} (sync)
    async def patch_key(self, pool: str, bucket: str, key: str, body: dict, project: str = "default") -> EmptySyncResponse:
        return await self._client.patch(
            f"/1.0/storage-pools/{pool}/buckets/{bucket}/keys/{key}",
            json_body=body,
            params={"project": project},
        )

    # DELETE .../keys/{key} (sync)
    async def delete_key(self, pool: str, bucket: str, key: str, project: str = "default") -> EmptySyncResponse:
        return await self._client.delete(
            f"/1.0/storage-pools/{pool}/buckets/{bucket}/keys/{key}",
            params={"project": project},
        )
