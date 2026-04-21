from models.emptySyncRepo_model import EmptySyncResponse
from models.instance_model import InstanceMetadata
from utility.rest_client import IncusRestClient


class InstancesMetadataController:
    def __init__(self, client: IncusRestClient):
        self._client = client

    # GET /1.0/instances/{name}/metadata (sync)
    async def get_metadata(self, name: str, project: str = "default") -> InstanceMetadata:
        return await self._client.get(
            f"/1.0/instances/{name}/metadata",
            params={"project": project},
        )

    # PUT /1.0/instances/{name}/metadata (sync)
    async def update_metadata(self, name: str, body: dict, project: str = "default") -> EmptySyncResponse:
        return await self._client.put(
            f"/1.0/instances/{name}/metadata",
            json_body=body,
            params={"project": project},
        )

    # PATCH /1.0/instances/{name}/metadata (sync)
    async def patch_metadata(self, name: str, body: dict, project: str = "default") -> EmptySyncResponse:
        return await self._client.patch(
            f"/1.0/instances/{name}/metadata",
            json_body=body,
            params={"project": project},
        )

    # GET /1.0/instances/{name}/metadata/templates (sync, list)
    async def list_templates(self, name: str, project: str = "default") -> list[str]:
        return await self._client.get(
            f"/1.0/instances/{name}/metadata/templates",
            params={"project": project},
        )

    # GET /1.0/instances/{name}/metadata/templates?path=... (raw)
    async def get_template(self, name: str, path: str, project: str = "default") -> bytes:
        return await self._client.get(
            f"/1.0/instances/{name}/metadata/templates",
            params={"path": path, "project": project},
            raw=True,
        )

    # POST /1.0/instances/{name}/metadata/templates?path=... (raw upload)
    async def put_template(self, name: str, path: str, content: bytes, project: str = "default") -> EmptySyncResponse:
        return await self._client.post_raw(
            f"/1.0/instances/{name}/metadata/templates",
            content=content,
            params={"path": path, "project": project},
        )

    # DELETE /1.0/instances/{name}/metadata/templates?path=... (sync)
    async def delete_template(self, name: str, path: str, project: str = "default") -> EmptySyncResponse:
        return await self._client.delete(
            f"/1.0/instances/{name}/metadata/templates",
            params={"path": path, "project": project},
        )
