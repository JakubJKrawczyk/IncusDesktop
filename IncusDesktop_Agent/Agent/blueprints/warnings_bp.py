# blueprints/warnings_bp.py
from flask import Blueprint, current_app, jsonify, request

from Agent.controllers.incus.warnings import WarningsController


bp = Blueprint("warnings", __name__, url_prefix="/warnings")


def _ctrl() -> WarningsController:
    return WarningsController(current_app.extensions["incus"])


@bp.get("")
async def list_warnings():
    recursion = int(request.args.get("recursion", 0))
    project = request.args.get("project")
    return jsonify(await _ctrl().list_warnings(recursion=recursion, project=project))


@bp.get("/<uuid>")
async def warning_info(uuid: str):
    return jsonify(await _ctrl().warning_info(uuid=uuid))


@bp.put("/<uuid>")
async def update_warning(uuid: str):
    body = request.get_json(force=True)
    await _ctrl().update_warning(uuid=uuid, body=body)
    return "", 200


@bp.delete("/<uuid>")
async def delete_warning(uuid: str):
    await _ctrl().delete_warning(uuid=uuid)
    return "", 200
