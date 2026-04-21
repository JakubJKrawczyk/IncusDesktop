from models.certificate_model import CertificateModel
from models.emptySyncRepo_model import EmptySyncResponse
from utility.rest_client import IncusRestClient


class CertificatesController:
    def __init__(self, client: IncusRestClient):
        self._client = client

    # GET /1.0/certificates (sync)
    async def list_certificates(self, recursion: int = 0, public: bool = False) -> list[CertificateModel]:
        params: dict = {"recursion": recursion}
        if public:
            params["public"] = ""
        return await self._client.get("/1.0/certificates", params=params)

    # POST /1.0/certificates (sync)
    async def create_certificate(self, body: dict, public: bool = False) -> EmptySyncResponse:
        params: dict = {}
        if public:
            params["public"] = ""
        return await self._client.post("/1.0/certificates", json_body=body, params=params or None)

    # GET /1.0/certificates/{fingerprint} (sync)
    async def certificate_info(self, fingerprint: str) -> CertificateModel:
        return await self._client.get(f"/1.0/certificates/{fingerprint}")

    # PUT /1.0/certificates/{fingerprint} (sync)
    async def update_certificate(self, fingerprint: str, body: dict) -> EmptySyncResponse:
        return await self._client.put(f"/1.0/certificates/{fingerprint}", json_body=body)

    # PATCH /1.0/certificates/{fingerprint} (sync)
    async def patch_certificate(self, fingerprint: str, body: dict) -> EmptySyncResponse:
        return await self._client.patch(f"/1.0/certificates/{fingerprint}", json_body=body)

    # DELETE /1.0/certificates/{fingerprint} (sync)
    async def delete_certificate(self, fingerprint: str) -> EmptySyncResponse:
        return await self._client.delete(f"/1.0/certificates/{fingerprint}")
