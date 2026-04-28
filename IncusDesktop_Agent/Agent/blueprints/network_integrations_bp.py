# blueprints/network_integrations_bp.py
from flask import Blueprint, current_app, jsonify, request

from Agent.controllers.incus.network_integrations import NetworkIntegrationsController


bp = Blueprint("network_integrations", __name__, url_prefix="/network-integrations")


def _ctrl() -> NetworkIntegrationsController:
    return NetworkIntegrationsController(current_app.extensions["incus"])


@bp.get("")
async def list_integrations():
    recursion = int(request.args.get("recursion", 0))
    return jsonify(await _ctrl().list_integrations(recursion=recursion))


@bp.post("")
async def create_integration():
    body = request.get_json(force=True)
    await _ctrl().create_integration(body=body)
    return "", 200


@bp.get("/<name>")
async def integration_info(name: str):
    return jsonify(await _ctrl().integration_info(name=name))


@bp.put("/<name>")
async def update_integration(name: str):
    body = request.get_json(force=True)
    await _ctrl().update_integration(name=name, body=body)
    return "", 200


@bp.patch("/<name>")
async def patch_integration(name: str):
    body = request.get_json(force=True)
    await _ctrl().patch_integration(name=name, body=body)
    return "", 204


@bp.post("/<name>")
async def rename_integration(name: str):
    body = request.get_json(force=True)
    await _ctrl().rename_integration(name=name, new_name=body["name"])
    return "", 200


@bp.delete("/<name>")
async def delete_integration(name: str):
    await _ctrl().delete_integration(name=name)
    return "", 200
