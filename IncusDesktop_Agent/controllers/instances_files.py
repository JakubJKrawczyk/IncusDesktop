from models.emptySyncRepo_model import EmptySyncResponse
from utility.rest_client import IncusRestClient


class InstancesFilesController:
    def __init__(self, client: IncusRestClient):
        self._client = client

    # GET /1.0/instances/{name}/files?path=/etc/hosts
    def get_file(self, name: str, path: str, project: str = "default") -> tuple[bytes, dict]:
        """
        Zwraca (content, headers). Headers zawieraja:
          X-Incus-type: "file" | "directory" | "symlink"
          X-Incus-uid, X-Incus-gid, X-Incus-mode, X-Incus-modified
        Dla directory content to JSON array nazw plikow (bytes z JSONem).
        Dla pliku content to raw bytes.
        """
        return self._client.get_raw_with_headers(
            f"/1.0/instances/{name}/files",
            params={"path": path, "project": project},
        )

    # HEAD /1.0/instances/{name}/files?path=...
    def stat_file(self, name: str, path: str, project: str = "default") -> dict:
        """Tylko metadata (headers), bez body."""
        return self._client.head(
            f"/1.0/instances/{name}/files",
            params={"path": path, "project": project},
        )

    # POST /1.0/instances/{name}/files?path=...
    def put_file(
        self,
        name: str,
        path: str,
        content: bytes,
        *,
        uid: int | None = None,
        gid: int | None = None,
        mode: int | None = None,  # np. 0o644
        type_: str = "file",      # "file" | "symlink" | "directory"
        write_mode: str = "overwrite",  # "overwrite" | "append"
        project: str = "default",
    ) -> EmptySyncResponse:
        headers: dict[str, str] = {"X-Incus-type": type_, "X-Incus-write": write_mode}
        if uid is not None:
            headers["X-Incus-uid"] = str(uid)
        if gid is not None:
            headers["X-Incus-gid"] = str(gid)
        if mode is not None:
            headers["X-Incus-mode"] = str(mode)

        return self._client.post_raw(
            f"/1.0/instances/{name}/files",
            content=content,
            params={"path": path, "project": project},
            headers=headers,
        )

    # DELETE /1.0/instances/{name}/files?path=...
    def delete_file(
        self,
        name: str,
        path: str,
        recursive: bool = False,
        project: str = "default",
    ) -> EmptySyncResponse:
        headers = {"X-Incus-force": "true"} if recursive else None
        return self._client.delete_with_headers(
            f"/1.0/instances/{name}/files",
            params={"path": path, "project": project},
            headers=headers,
        )

    # GET /1.0/instances/{name}/sftp
    def sftp_endpoint(self, name: str, project: str = "default") -> dict:
        """
        UWAGA: Ten endpoint robi HTTP 101 Upgrade do protokołu SFTP.
        Przez zwykly REST client to sie NIE UDA - wymaga raw socket hijacking.
        Zostawiam jako placeholder - realnie nie uzywalne bez dedykowanej obslugi.
        """
        raise NotImplementedError(
            "SFTP endpoint wymaga HTTP upgrade - uzyj osobnego sftp clienta albo WS proxy"
        )