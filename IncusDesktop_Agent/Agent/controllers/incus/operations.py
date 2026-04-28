from Agent.models.emptySyncRepo_model import EmptySyncResponse
from Agent.models.operation_model import OperationModel
from Agent.utility.rest_client import IncusRestClient


class OperationsController:
    def __init__(self, client: IncusRestClient):
        self._client = client

    # GET /1.0/operations (sync)
    async def list_operations(
        self,
        recursion: int = 0,
        project: str = "default",
        all_projects: bool = False,
    ) -> list[OperationModel]:
        return await self._client.get(
            "/1.0/operations",
            params={
                "recursion": recursion,
                "project": project,
                "all-projects": "true" if all_projects else None,
            },
        )

    # GET /1.0/operations/{id} (sync)
    async def operation_info(self, id: str) -> OperationModel:
        return await self._client.get(f"/1.0/operations/{id}")

    # DELETE /1.0/operations/{id} (sync)
    async def cancel_operation(self, id: str) -> EmptySyncResponse:
        return await self._client.delete(f"/1.0/operations/{id}")

    # GET /1.0/operations/{id}/wait (sync)
    async def wait_operation(self, id: str, timeout: int = 60, public: bool = False) -> OperationModel:
        params: dict = {"timeout": timeout}
        if public:
            params["public"] = ""
        return await self._client.get(f"/1.0/operations/{id}/wait", params=params)

    # GET /1.0/operations/{id}/websocket (placeholder 501)
    async def operation_websocket(self, id: str, secret: str | None = None, public: bool = False):
        raise NotImplementedError("operation websocket requires WebSocket handling")
