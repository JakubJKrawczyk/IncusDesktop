# blueprints/certificates_bp.py
from flask import Blueprint, current_app, jsonify, request

from Agent.controllers.incus.certificates import CertificatesController


bp = Blueprint("certificates", __name__, url_prefix="/certificates")


def _ctrl() -> CertificatesController:
    return CertificatesController(current_app.extensions["incus"])


@bp.get("")
async def list_certificates():
    recursion = int(request.args.get("recursion", 0))
    public = "public" in request.args
    return jsonify(await _ctrl().list_certificates(recursion=recursion, public=public))


@bp.post("")
async def create_certificate():
    public = "public" in request.args
    body = request.get_json(force=True)
    await _ctrl().create_certificate(body=body, public=public)
    return "", 200


@bp.get("/<fingerprint>")
async def certificate_info(fingerprint: str):
    return jsonify(await _ctrl().certificate_info(fingerprint=fingerprint))


@bp.put("/<fingerprint>")
async def update_certificate(fingerprint: str):
    body = request.get_json(force=True)
    await _ctrl().update_certificate(fingerprint=fingerprint, body=body)
    return "", 200


@bp.patch("/<fingerprint>")
async def patch_certificate(fingerprint: str):
    body = request.get_json(force=True)
    await _ctrl().patch_certificate(fingerprint=fingerprint, body=body)
    return "", 204


@bp.delete("/<fingerprint>")
async def delete_certificate(fingerprint: str):
    await _ctrl().delete_certificate(fingerprint=fingerprint)
    return "", 200
