# controllers/instances_exec.py
from models.operation_model import OperationModel
from utility.rest_client import IncusRestClient


class InstancesExecController:
    def __init__(self, client: IncusRestClient):
        self._client = client

    # ─── EXEC ──────────────────────────────────────────────────────────

    # POST /1.0/instances/{name}/exec  (async - Operation z websocket URLami w metadata.fds)
    def exec_command(self, name: str, body: dict, project: str = "default") -> OperationModel:
        """
        body = {
            "command": ["bash", "-c", "ls"],    # wymagane
            "environment": {"FOO": "bar"},      # opcjonalne
            "cwd": "/root",                     # opcjonalne
            "user": 0,                          # UID (opcjonalne)
            "group": 0,                         # GID (opcjonalne)
            "interactive": False,               # False=3 WS (stdin/stdout/stderr), True=1 PTY
            "wait-for-websocket": True,         # czekaj na WS connect przed spawn
            "record-output": False,             # zapisz stdout/stderr do plikow (non-interactive)
            "width": 80, "height": 24,          # tylko interactive
        }
        Zwraca Operation - klient laczy sie do websocketow z metadata.fds.
        """
        return self._client.post(
            f"/1.0/instances/{name}/exec",
            json_body=body,
            params={"project": project},
            wait=False,  # NIE czekamy - klient musi sie podpiac do WS
        )

    # ─── CONSOLE ───────────────────────────────────────────────────────

    # POST /1.0/instances/{name}/console  (async - Operation z WS)
    def console_attach(self, name: str, body: dict, project: str = "default") -> OperationModel:
        """
        body = {
            "type": "console",   # "console" (tty, kontenery+VM) | "vga" (VGA framebuffer, tylko VM)
            "width": 80, "height": 24,
        }
        """
        return self._client.post(
            f"/1.0/instances/{name}/console",
            json_body=body,
            params={"project": project},
            wait=False,
        )

    # GET /1.0/instances/{name}/console  (raw bytes - zapisany console log)
    def get_console_log(self, name: str, project: str = "default") -> bytes:
        return self._client.get(
            f"/1.0/instances/{name}/console",
            params={"project": project},
            raw=True
        )

    # DELETE /1.0/instances/{name}/console  (wyczysc log)
    def clear_console_log(self, name: str, project: str = "default") -> None:
        self._client.delete(
            f"/1.0/instances/{name}/console",
            params={"project": project},
        )

    # ─── LOGS (systemowe logi instancji) ───────────────────────────────

    # GET /1.0/instances/{name}/logs
    def list_logs(self, name: str, project: str = "default") -> list[str]:
        return self._client.get(
            f"/1.0/instances/{name}/logs",
            params={"project": project},
        )

    # GET /1.0/instances/{name}/logs/{filename}  (raw bytes)
    def get_log(self, name: str, filename: str, project: str = "default") -> bytes:
        return self._client.get(
            f"/1.0/instances/{name}/logs/{filename}",
            params={"project": project},
            raw=True
        )

    # DELETE /1.0/instances/{name}/logs/{filename}
    def delete_log(self, name: str, filename: str, project: str = "default") -> None:
        self._client.delete(
            f"/1.0/instances/{name}/logs/{filename}",
            params={"project": project},
        )

    # ─── EXEC OUTPUT (zapisane stdout/stderr z exec --record-output) ───

    # GET /1.0/instances/{name}/logs/exec-output
    def list_exec_outputs(self, name: str, project: str = "default") -> list[str]:
        return self._client.get(
            f"/1.0/instances/{name}/logs/exec-output",
            params={"project": project},
        )

    # GET /1.0/instances/{name}/logs/exec-output/{filename}  (raw bytes)
    def get_exec_output(self, name: str, filename: str, project: str = "default") -> bytes:
        return self._client.get(
            f"/1.0/instances/{name}/logs/exec-output/{filename}",
            params={"project": project},
            raw=True
        )

    # DELETE /1.0/instances/{name}/logs/exec-output/{filename}
    def delete_exec_output(self, name: str, filename: str, project: str = "default") -> None:
        self._client.delete(
            f"/1.0/instances/{name}/logs/exec-output/{filename}",
            params={"project": project},
        )