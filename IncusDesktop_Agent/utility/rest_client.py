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
        transport = httpx.AsyncHTTPTransport(uds=socket_path)

        self._client = httpx.AsyncClient(
            transport=transport,
            timeout=timeout,
            base_url="http://localhost",
            headers={"Content-Type": "application/json"},
        )

    async def close(self) -> None:
        await self._client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_):
        await self.close()

    async def get(self, path: str, params: dict | None = None, *, raw: bool = False):
        return await self._request("GET", path, params=params, raw=raw)

    async def put(self, path: str, json_body: Any = None, *, params: dict | None = None, wait: bool = True, wait_timeout: int = 60):
        return await self._request("PUT", path, json_body=json_body, params=params, wait=wait, wait_timeout=wait_timeout)

    async def post(self, path: str, json_body: Any = None, *, params: dict | None = None, wait: bool = True, wait_timeout: int = 60):
        return await self._request("POST", path, json_body=json_body, params=params, wait=wait, wait_timeout=wait_timeout)

    async def patch(self, path: str, json_body: Any = None, *, params: dict | None = None, wait: bool = True, wait_timeout: int = 60):
        return await self._request("PATCH", path, json_body=json_body, params=params, wait=wait, wait_timeout=wait_timeout)

    async def delete(self, path: str, *, params: dict | None = None, wait: bool = True, wait_timeout: int = 60):
        return await self._request("DELETE", path, params=params, wait=wait, wait_timeout=wait_timeout)

    # --- Internal ---

    async def _request(
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
            response = await self._client.request(method, path, params=params, json=json_body)
        except httpx.RequestError as exc:
            raise IncusError(f"transport error: {exc}") from exc

        if raw:
            if response.status_code >= 400:
                raise IncusError(f"http {response.status_code}: {response.text[:200]}")
            return response.content

        return await self._handle_envelope(response, wait=wait, wait_timeout=wait_timeout)

    async def _handle_envelope(
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
            return await self._wait_operation(operation_url, wait_timeout)

        raise IncusError(f"unexpected response type: {response_type!r}")

    async def _wait_operation(self, operation_url: str, wait_timeout: int):
        wait_response = await self._client.get(
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

    async def head(self, path: str, params: dict | None = None, *, headers: dict | None = None):
        """HEAD — zwraca tylko dict nagłówków response, nie body."""
        try:
            response = await self._client.request("HEAD", path, params=params, headers=headers)
        except httpx.RequestError as exc:
            raise IncusError(f"transport error: {exc}") from exc
        if response.status_code >= 400:
            raise IncusError(f"http {response.status_code}")
        return dict(response.headers)

    async def get_raw_with_headers(self, path: str, params: dict | None = None, *, headers: dict | None = None) -> tuple[
        bytes, dict]:
        """GET raw z headerami — dla /files gdzie metadata jest w X-Incus-*."""
        try:
            response = await self._client.request("GET", path, params=params, headers=headers)
        except httpx.RequestError as exc:
            raise IncusError(f"transport error: {exc}") from exc
        if response.status_code >= 400:
            raise IncusError(f"http {response.status_code}: {response.text[:200]}")
        return response.content, dict(response.headers)

    async def post_raw(self, path: str, content: bytes, *, params: dict | None = None, headers: dict | None = None):
        """POST raw bytes (octet-stream) — upload plikow."""
        req_headers = {"Content-Type": "application/octet-stream"}
        if headers:
            req_headers.update(headers)
        try:
            response = await self._client.request("POST", path, params=params, headers=req_headers, content=content)
        except httpx.RequestError as exc:
            raise IncusError(f"transport error: {exc}") from exc
        return await self._handle_envelope(response, wait=False, wait_timeout=0)

    async def delete_with_headers(self, path: str, *, params: dict | None = None, headers: dict | None = None):
        """DELETE z custom headers — dla X-Incus-force przy recursive delete."""
        try:
            response = await self._client.request("DELETE", path, params=params, headers=headers)
        except httpx.RequestError as exc:
            raise IncusError(f"transport error: {exc}") from exc
        return await self._handle_envelope(response, wait=False, wait_timeout=0)
