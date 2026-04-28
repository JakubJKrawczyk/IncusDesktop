from Agent.models.emptySyncRepo_model import EmptySyncResponse
from Agent.models.image_model import ImageAliasModel, ImageModel
from Agent.models.operation_model import OperationModel
from Agent.utility.rest_client import IncusRestClient


class ImagesController:
    def __init__(self, client: IncusRestClient):
        self._client = client

    # GET /1.0/images (sync)
    async def list_images(
        self,
        recursion: int = 0,
        public: bool = False,
        project: str = "default",
        filter: str | None = None,
        all_projects: bool = False,
    ) -> list[ImageModel]:
        params: dict = {
            "recursion": recursion,
            "project": project,
            "filter": filter,
            "all-projects": "true" if all_projects else None,
        }
        if public:
            params["public"] = ""
        return await self._client.get("/1.0/images", params=params)

    # POST /1.0/images (async, JSON)
    async def create_image(self, body: dict, project: str = "default") -> OperationModel:
        return await self._client.post(
            "/1.0/images",
            json_body=body,
            params={"project": project},
        )

    # POST /1.0/images (async, octet-stream/multipart)
    async def upload_image(self, content: bytes, headers: dict | None = None, project: str = "default") -> OperationModel:
        return await self._client.post_raw(
            "/1.0/images",
            content=content,
            params={"project": project},
            headers=headers,
        )

    # GET /1.0/images/{fingerprint} (sync)
    async def image_info(self, fingerprint: str, public: bool = False, project: str = "default") -> ImageModel:
        params: dict = {"project": project}
        if public:
            params["public"] = ""
        return await self._client.get(f"/1.0/images/{fingerprint}", params=params)

    # PUT /1.0/images/{fingerprint} (sync)
    async def update_image(self, fingerprint: str, body: dict, project: str = "default") -> EmptySyncResponse:
        return await self._client.put(
            f"/1.0/images/{fingerprint}",
            json_body=body,
            params={"project": project},
        )

    # PATCH /1.0/images/{fingerprint} (sync)
    async def patch_image(self, fingerprint: str, body: dict, project: str = "default") -> EmptySyncResponse:
        return await self._client.patch(
            f"/1.0/images/{fingerprint}",
            json_body=body,
            params={"project": project},
        )

    # DELETE /1.0/images/{fingerprint} (async)
    async def delete_image(self, fingerprint: str, project: str = "default") -> OperationModel:
        return await self._client.delete(
            f"/1.0/images/{fingerprint}",
            params={"project": project},
        )

    # GET /1.0/images/{fingerprint}/export (raw)
    async def export_image(self, fingerprint: str, public: bool = False, project: str = "default") -> bytes:
        params: dict = {"project": project}
        if public:
            params["public"] = ""
        return await self._client.get(
            f"/1.0/images/{fingerprint}/export",
            params=params,
            raw=True,
        )

    # POST /1.0/images/{fingerprint}/export (async)
    async def push_export_image(self, fingerprint: str, body: dict, project: str = "default") -> OperationModel:
        return await self._client.post(
            f"/1.0/images/{fingerprint}/export",
            json_body=body,
            params={"project": project},
        )

    # POST /1.0/images/{fingerprint}/refresh (async)
    async def refresh_image(self, fingerprint: str, project: str = "default") -> OperationModel:
        return await self._client.post(
            f"/1.0/images/{fingerprint}/refresh",
            params={"project": project},
        )

    # POST /1.0/images/{fingerprint}/secret (async)
    async def create_image_secret(self, fingerprint: str, project: str = "default") -> OperationModel:
        return await self._client.post(
            f"/1.0/images/{fingerprint}/secret",
            params={"project": project},
        )

    # GET /1.0/images/aliases (sync)
    async def list_aliases(self, recursion: int = 0, project: str = "default") -> list[ImageAliasModel]:
        return await self._client.get(
            "/1.0/images/aliases",
            params={"recursion": recursion, "project": project},
        )

    # POST /1.0/images/aliases (sync)
    async def create_alias(self, body: dict, project: str = "default") -> EmptySyncResponse:
        return await self._client.post(
            "/1.0/images/aliases",
            json_body=body,
            params={"project": project},
        )

    # GET /1.0/images/aliases/{name} (sync)
    async def alias_info(self, name: str, public: bool = False, project: str = "default") -> ImageAliasModel:
        params: dict = {"project": project}
        if public:
            params["public"] = ""
        return await self._client.get(f"/1.0/images/aliases/{name}", params=params)

    # PUT /1.0/images/aliases/{name} (sync)
    async def update_alias(self, name: str, body: dict, project: str = "default") -> EmptySyncResponse:
        return await self._client.put(
            f"/1.0/images/aliases/{name}",
            json_body=body,
            params={"project": project},
        )

    # PATCH /1.0/images/aliases/{name} (sync)
    async def patch_alias(self, name: str, body: dict, project: str = "default") -> EmptySyncResponse:
        return await self._client.patch(
            f"/1.0/images/aliases/{name}",
            json_body=body,
            params={"project": project},
        )

    # POST /1.0/images/aliases/{name} (sync)
    async def rename_alias(self, name: str, new_name: str, project: str = "default") -> EmptySyncResponse:
        return await self._client.post(
            f"/1.0/images/aliases/{name}",
            json_body={"name": new_name},
            params={"project": project},
        )

    # DELETE /1.0/images/aliases/{name} (sync)
    async def delete_alias(self, name: str, project: str = "default") -> EmptySyncResponse:
        return await self._client.delete(
            f"/1.0/images/aliases/{name}",
            params={"project": project},
        )
