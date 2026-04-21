from models.emptySyncRepo_model import EmptySyncResponse
from models.resources_model import ResourcesModel
from models.server_model import ServerModel
from utility.rest_client import IncusRestClient


class ServerController:
    def __init__(self, client: IncusRestClient):
        self._client = client

    # GET / (sync)
    async def root(self) -> list[str]:
        return await self._client.get("/")

    # GET /1.0 (sync)
    async def server_info(self, public: bool = False) -> ServerModel:
        params: dict = {}
        if public:
            params["public"] = ""
        return await self._client.get("/1.0", params=params or None)

    # PUT /1.0 (sync)
    async def update_server(self, body: dict) -> EmptySyncResponse:
        return await self._client.put("/1.0", json_body=body)

    # PATCH /1.0 (sync)
    async def patch_server(self, body: dict) -> EmptySyncResponse:
        return await self._client.patch("/1.0", json_body=body)

    # GET /1.0/events (WebSocket - placeholder 501)
    async def events_stream(self, type: str | None = None, project: str | None = None):
        raise NotImplementedError("events stream requires WebSocket handling")

    # GET /1.0/resources (sync)
    async def resources(self) -> ResourcesModel:
        return await self._client.get("/1.0/resources")

    # GET /1.0/metrics (raw text)
    async def metrics(self, project: str | None = None) -> bytes:
        return await self._client.get(
            "/1.0/metrics",
            params={"project": project},
            raw=True,
        )

    # GET /1.0/metadata/configuration (sync)
    async def metadata_configuration(self) -> dict:
        return await self._client.get("/1.0/metadata/configuration")
