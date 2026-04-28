# blueprints/network_zones_records_bp.py
from flask import Blueprint, current_app, jsonify, request

from Agent.controllers.incus.network_zones_records import NetworkZonesRecordsController


bp = Blueprint("network_zones_records", __name__, url_prefix="/network-zones")


def _ctrl() -> NetworkZonesRecordsController:
    return NetworkZonesRecordsController(current_app.extensions["incus"])


@bp.get("/<zone>/records")
async def list_records(zone: str):
    project = request.args.get("project", "default")
    recursion = int(request.args.get("recursion", 0))
    return jsonify(await _ctrl().list_records(zone=zone, recursion=recursion, project=project))


@bp.post("/<zone>/records")
async def create_record(zone: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().create_record(zone=zone, body=body, project=project)
    return "", 200


@bp.get("/<zone>/records/<name>")
async def record_info(zone: str, name: str):
    project = request.args.get("project", "default")
    return jsonify(await _ctrl().record_info(zone=zone, name=name, project=project))


@bp.put("/<zone>/records/<name>")
async def update_record(zone: str, name: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().update_record(zone=zone, name=name, body=body, project=project)
    return "", 200


@bp.patch("/<zone>/records/<name>")
async def patch_record(zone: str, name: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().patch_record(zone=zone, name=name, body=body, project=project)
    return "", 204


@bp.delete("/<zone>/records/<name>")
async def delete_record(zone: str, name: str):
    project = request.args.get("project", "default")
    await _ctrl().delete_record(zone=zone, name=name, project=project)
    return "", 200
