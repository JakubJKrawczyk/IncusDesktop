from models.emptySyncRepo_model import EmptySyncResponse
from utility.rest_client import IncusRestClient


class InstancesFilesController:
    def __init__(self, client: IncusRestClient):
        self._client = client

    # GET /1.0/instances/{name}/files (raw+headers)
    async def get_file(self, name: str, path: str, project: str = "default") -> tuple[bytes, dict]:
        return await self._client.get_raw_with_headers(
            f"/1.0/instances/{name}/files",
            params={"path": path, "project": project},
        )

    # HEAD /1.0/instances/{name}/files (raw headers)
    async def stat_file(self, name: str, path: str, project: str = "default") -> dict:
        return await self._client.head(
            f"/1.0/instances/{name}/files",
            params={"path": path, "project": project},
        )

    # POST /1.0/instances/{name}/files (raw)
    async def put_file(
        self,
        name: str,
        path: str,
        content: bytes,
        *,
        uid: int | None = None,
        gid: int | None = None,
        mode: int | None = None,
        type_: str = "file",
        write_mode: str = "overwrite",
        project: str = "default",
    ) -> EmptySyncResponse:
        headers: dict[str, str] = {"X-Incus-type": type_, "X-Incus-write": write_mode}
        if uid is not None:
            headers["X-Incus-uid"] = str(uid)
        if gid is not None:
            headers["X-Incus-gid"] = str(gid)
        if mode is not None:
            headers["X-Incus-mode"] = str(mode)

        return await self._client.post_raw(
            f"/1.0/instances/{name}/files",
            content=content,
            params={"path": path, "project": project},
            headers=headers,
        )

    # DELETE /1.0/instances/{name}/files (sync)
    async def delete_file(
        self,
        name: str,
        path: str,
        recursive: bool = False,
        project: str = "default",
    ) -> EmptySyncResponse:
        headers = {"X-Incus-force": "true"} if recursive else None
        return await self._client.delete_with_headers(
            f"/1.0/instances/{name}/files",
            params={"path": path, "project": project},
            headers=headers,
        )

    # GET /1.0/instances/{name}/sftp (placeholder 501)
    async def sftp_endpoint(self, name: str, project: str = "default") -> dict:
        raise NotImplementedError(
            "SFTP endpoint wymaga HTTP upgrade - uzyj osobnego sftp clienta albo WS proxy"
        )
