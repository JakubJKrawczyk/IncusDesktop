# blueprints/network_zones_bp.py
from flask import Blueprint, current_app, jsonify, request

from controllers.incus.network_zones import NetworkZonesController


bp = Blueprint("network_zones", __name__, url_prefix="/network-zones")


def _ctrl() -> NetworkZonesController:
    return NetworkZonesController(current_app.extensions["incus"])


@bp.get("")
async def list_zones():
    project = request.args.get("project", "default")
    recursion = int(request.args.get("recursion", 0))
    return jsonify(await _ctrl().list_zones(recursion=recursion, project=project))


@bp.post("")
async def create_zone():
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().create_zone(body=body, project=project)
    return "", 200


@bp.get("/<name>")
async def zone_info(name: str):
    project = request.args.get("project", "default")
    return jsonify(await _ctrl().zone_info(name=name, project=project))


@bp.put("/<name>")
async def update_zone(name: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().update_zone(name=name, body=body, project=project)
    return "", 200


@bp.patch("/<name>")
async def patch_zone(name: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().patch_zone(name=name, body=body, project=project)
    return "", 204


@bp.delete("/<name>")
async def delete_zone(name: str):
    project = request.args.get("project", "default")
    await _ctrl().delete_zone(name=name, project=project)
    return "", 200
