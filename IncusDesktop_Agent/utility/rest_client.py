import json
from typing import Any
import httpx

from models.consts import StatusCode


class IncusError(Exception):
    code = "INCUS_ERROR"
    status = 500


class IncusRestClient:
    DEFAULT_SOCKET = "/var/lib/incus/unix.socket"

    def __init__(self, socket_path: str = DEFAULT_SOCKET, timeout: float = 30.0):
        transport = httpx.HTTPTransport(uds=socket_path)

        self._client = httpx.Client(
            transport=transport,
            timeout=timeout,
            base_url="http://localhost",
            headers={"Content-Type": "application/json"},
        )

    def close(self) -> None:
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    def get(self, path: str, params: dict | None = None, *, raw: bool = False):
        return self._request("GET", path, params=params, raw=raw)

    def put(self, path: str, json_body: Any = None, *, params: dict | None = None, wait: bool = True, wait_timeout: int = 60):
        return self._request("PUT", path, json_body=json_body, params=params, wait=wait, wait_timeout=wait_timeout)

    def post(self, path: str, json_body: Any = None, *, params: dict | None = None, wait: bool = True, wait_timeout: int = 60):
        return self._request("POST", path, json_body=json_body, params=params, wait=wait, wait_timeout=wait_timeout)

    def patch(self, path: str, json_body: Any = None, *, params: dict | None = None, wait: bool = True, wait_timeout: int = 60):
        return self._request("PATCH", path, json_body=json_body, params=params, wait=wait, wait_timeout=wait_timeout)

    def delete(self, path: str, *, params: dict | None = None, wait: bool = True, wait_timeout: int = 60):
        return self._request("DELETE", path, params=params, wait=wait, wait_timeout=wait_timeout)

    # --- Internal ---

    def _request(
            self,
            method: str,
            path: str,
            *,
            params: dict | None = None,
            json_body: Any = None,
            wait: bool = True,
            wait_timeout: int = 60,
            raw: bool = False,
    ):
        try:
            response = self._client.request(method, path, params=params, json=json_body)
        except httpx.RequestError as exc:
            raise IncusError(f"transport error: {exc}") from exc

        if raw:
            if response.status_code >= 400:
                raise IncusError(f"http {response.status_code}: {response.text[:200]}")
            return response.content

        return self._handle_envelope(response, wait=wait, wait_timeout=wait_timeout)

    def _handle_envelope(
            self,
            response: httpx.Response,
            *,
            wait: bool = True,
            wait_timeout: int = 60
    ):
        try:
            payload = response.json()
        except json.JSONDecodeError:
            raise IncusError(f"non-JSON response ({response.status_code}): {response.text[:200]}")

        response_type = payload.get("type")

        if response_type == "error":
            raise IncusError(
                f"{payload.get('error', 'unknown')} "
                f"(error_code={payload.get('error_code', self._parse_status_code(response.status_code))})"
            )

        if response_type == "sync":
            return payload.get("metadata")

        if response_type == "async":
            operation_url = payload.get("operation")
            if not operation_url:
                raise IncusError("async response without operation url")
            if not wait:
                return payload
            return self._wait_operation(operation_url, wait_timeout)

        raise IncusError(f"unexpected response type: {response_type!r}")

    def _wait_operation(self, operation_url: str, wait_timeout: int):
        wait_response = self._client.get(
            f"{operation_url}/wait",
            params={"timeout": wait_timeout},
        )
        try:
            payload = wait_response.json()
        except json.JSONDecodeError:
            raise IncusError(f"non-JSON wait response: {wait_response.text[:200]}")

        metadata = payload.get("metadata", {})

        if metadata.get("status") == "Failure":
            raise IncusError(f"operation failure: {metadata.get('err', 'unknown')}")

        return metadata

    @staticmethod
    def _parse_status_code(status_code: int) -> str:
        try:
            code_error = StatusCode.CODES[status_code]
        except KeyError:
            code_error = f"Not supported status code: {status_code}"
        return code_error