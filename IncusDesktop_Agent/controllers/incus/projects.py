from models.access_model import Access
from models.emptySyncRepo_model import EmptySyncResponse
from models.operation_model import OperationModel
from models.project_model import ProjectModel, ProjectState
from utility.rest_client import IncusRestClient


class ProjectsController:
    def __init__(self, client: IncusRestClient):
        self._client = client

    # GET /1.0/projects (sync)
    async def list_projects(self, recursion: int = 0, filter: str | None = None) -> list[ProjectModel]:
        return await self._client.get(
            "/1.0/projects",
            params={"recursion": recursion, "filter": filter},
        )

    # POST /1.0/projects (sync)
    async def create_project(self, body: dict) -> EmptySyncResponse:
        return await self._client.post("/1.0/projects", json_body=body)

    # GET /1.0/projects/{name} (sync)
    async def project_info(self, name: str) -> ProjectModel:
        return await self._client.get(f"/1.0/projects/{name}")

    # PUT /1.0/projects/{name} (sync)
    async def update_project(self, name: str, body: dict) -> EmptySyncResponse:
        return await self._client.put(f"/1.0/projects/{name}", json_body=body)

    # PATCH /1.0/projects/{name} (sync)
    async def patch_project(self, name: str, body: dict) -> EmptySyncResponse:
        return await self._client.patch(f"/1.0/projects/{name}", json_body=body)

    # POST /1.0/projects/{name} (async, rename)
    async def rename_project(self, name: str, new_name: str) -> OperationModel:
        return await self._client.post(
            f"/1.0/projects/{name}",
            json_body={"name": new_name},
        )

    # DELETE /1.0/projects/{name} (sync)
    async def delete_project(self, name: str) -> EmptySyncResponse:
        return await self._client.delete(f"/1.0/projects/{name}")

    # GET /1.0/projects/{name}/access (sync)
    async def project_access(self, name: str) -> Access:
        return await self._client.get(f"/1.0/projects/{name}/access")

    # GET /1.0/projects/{name}/state (sync)
    async def project_state(self, name: str) -> ProjectState:
        return await self._client.get(f"/1.0/projects/{name}/state")
