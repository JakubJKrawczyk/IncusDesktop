from Agent.models.emptySyncRepo_model import EmptySyncResponse
from Agent.models.profile_model import ProfileModel
from Agent.utility.rest_client import IncusRestClient


class ProfilesController:
    def __init__(self, client: IncusRestClient):
        self._client = client

    # GET /1.0/profiles (sync)
    async def list_profiles(
        self,
        recursion: int = 0,
        project: str = "default",
        filter: str | None = None,
    ) -> list[ProfileModel]:
        return await self._client.get(
            "/1.0/profiles",
            params={"recursion": recursion, "project": project, "filter": filter},
        )

    # POST /1.0/profiles (sync)
    async def create_profile(self, body: dict, project: str = "default") -> EmptySyncResponse:
        return await self._client.post(
            "/1.0/profiles",
            json_body=body,
            params={"project": project},
        )

    # GET /1.0/profiles/{name} (sync)
    async def profile_info(self, name: str, project: str = "default") -> ProfileModel:
        return await self._client.get(
            f"/1.0/profiles/{name}",
            params={"project": project},
        )

    # PUT /1.0/profiles/{name} (sync)
    async def update_profile(self, name: str, body: dict, project: str = "default") -> EmptySyncResponse:
        return await self._client.put(
            f"/1.0/profiles/{name}",
            json_body=body,
            params={"project": project},
        )

    # PATCH /1.0/profiles/{name} (sync)
    async def patch_profile(self, name: str, body: dict, project: str = "default") -> EmptySyncResponse:
        return await self._client.patch(
            f"/1.0/profiles/{name}",
            json_body=body,
            params={"project": project},
        )

    # POST /1.0/profiles/{name} (sync, rename)
    async def rename_profile(self, name: str, new_name: str, project: str = "default") -> EmptySyncResponse:
        return await self._client.post(
            f"/1.0/profiles/{name}",
            json_body={"name": new_name},
            params={"project": project},
        )

    # DELETE /1.0/profiles/{name} (sync)
    async def delete_profile(self, name: str, project: str = "default") -> EmptySyncResponse:
        return await self._client.delete(
            f"/1.0/profiles/{name}",
            params={"project": project},
        )
