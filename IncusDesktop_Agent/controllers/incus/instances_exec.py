# controllers/instances_exec.py
from models.operation_model import OperationModel
from utility.rest_client import IncusRestClient


class InstancesExecController:
    def __init__(self, client: IncusRestClient):
        self._client = client

    # POST /1.0/instances/{name}/exec (async)
    async def exec_command(self, name: str, body: dict, project: str = "default") -> OperationModel:
        return await self._client.post(
            f"/1.0/instances/{name}/exec",
            json_body=body,
            params={"project": project},
            wait=False,
        )

    # POST /1.0/instances/{name}/console (async)
    async def console_attach(self, name: str, body: dict, project: str = "default") -> OperationModel:
        return await self._client.post(
            f"/1.0/instances/{name}/console",
            json_body=body,
            params={"project": project},
            wait=False,
        )

    # GET /1.0/instances/{name}/console (raw)
    async def get_console_log(self, name: str, project: str = "default") -> bytes:
        return await self._client.get(
            f"/1.0/instances/{name}/console",
            params={"project": project},
            raw=True,
        )

    # DELETE /1.0/instances/{name}/console (sync)
    async def clear_console_log(self, name: str, project: str = "default") -> None:
        await self._client.delete(
            f"/1.0/instances/{name}/console",
            params={"project": project},
        )

    # GET /1.0/instances/{name}/logs (sync)
    async def list_logs(self, name: str, project: str = "default") -> list[str]:
        return await self._client.get(
            f"/1.0/instances/{name}/logs",
            params={"project": project},
        )

    # GET /1.0/instances/{name}/logs/{filename} (raw)
    async def get_log(self, name: str, filename: str, project: str = "default") -> bytes:
        return await self._client.get(
            f"/1.0/instances/{name}/logs/{filename}",
            params={"project": project},
            raw=True,
        )

    # DELETE /1.0/instances/{name}/logs/{filename} (sync)
    async def delete_log(self, name: str, filename: str, project: str = "default") -> None:
        await self._client.delete(
            f"/1.0/instances/{name}/logs/{filename}",
            params={"project": project},
        )

    # GET /1.0/instances/{name}/logs/exec-output (sync)
    async def list_exec_outputs(self, name: str, project: str = "default") -> list[str]:
        return await self._client.get(
            f"/1.0/instances/{name}/logs/exec-output",
            params={"project": project},
        )

    # GET /1.0/instances/{name}/logs/exec-output/{filename} (raw)
    async def get_exec_output(self, name: str, filename: str, project: str = "default") -> bytes:
        return await self._client.get(
            f"/1.0/instances/{name}/logs/exec-output/{filename}",
            params={"project": project},
            raw=True,
        )

    # DELETE /1.0/instances/{name}/logs/exec-output/{filename} (sync)
    async def delete_exec_output(self, name: str, filename: str, project: str = "default") -> None:
        await self._client.delete(
            f"/1.0/instances/{name}/logs/exec-output/{filename}",
            params={"project": project},
        )
