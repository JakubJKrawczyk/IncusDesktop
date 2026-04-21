from models.emptySyncRepo_model import EmptySyncResponse
from models.warning_model import WarningModel
from utility.rest_client import IncusRestClient


class WarningsController:
    def __init__(self, client: IncusRestClient):
        self._client = client

    # GET /1.0/warnings (sync)
    async def list_warnings(self, recursion: int = 0, project: str | None = None) -> list[WarningModel]:
        return await self._client.get(
            "/1.0/warnings",
            params={"recursion": recursion, "project": project},
        )

    # GET /1.0/warnings/{uuid} (sync)
    async def warning_info(self, uuid: str) -> WarningModel:
        return await self._client.get(f"/1.0/warnings/{uuid}")

    # PUT /1.0/warnings/{uuid} (sync)
    async def update_warning(self, uuid: str, body: dict) -> EmptySyncResponse:
        return await self._client.put(f"/1.0/warnings/{uuid}", json_body=body)

    # DELETE /1.0/warnings/{uuid} (sync)
    async def delete_warning(self, uuid: str) -> EmptySyncResponse:
        return await self._client.delete(f"/1.0/warnings/{uuid}")
