# blueprints/instances_misc_bp.py
from flask import Blueprint, current_app, jsonify, request, Response

from controllers.incus.instances_misc import InstancesMiscController


bp = Blueprint("instances_misc", __name__, url_prefix="/instances")


def _ctrl() -> InstancesMiscController:
    return InstancesMiscController(current_app.extensions["incus"])


@bp.post("/<name>/bitmaps")
async def create_bitmap(name: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    return jsonify(await _ctrl().create_bitmap(name=name, body=body, project=project)), 202


@bp.get("/<name>/debug/memory")
async def debug_memory(name: str):
    project = request.args.get("project", "default")
    format_ = request.args.get("format")
    data = await _ctrl().debug_memory(name=name, format=format_, project=project)
    return Response(data, mimetype="application/octet-stream")


@bp.get("/<name>/debug/repair")
async def debug_repair(name: str):
    project = request.args.get("project", "default")
    return jsonify(await _ctrl().debug_repair(name=name, project=project))
