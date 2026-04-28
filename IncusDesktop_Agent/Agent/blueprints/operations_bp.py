# blueprints/operations_bp.py
from flask import Blueprint, current_app, jsonify, request

from Agent.controllers.incus.operations import OperationsController


bp = Blueprint("operations", __name__, url_prefix="/operations")


def _ctrl() -> OperationsController:
    return OperationsController(current_app.extensions["incus"])


@bp.get("")
async def list_operations():
    recursion = int(request.args.get("recursion", 0))
    project = request.args.get("project", "default")
    all_projects = request.args.get("all-projects") == "true"
    return jsonify(await _ctrl().list_operations(
        recursion=recursion, project=project, all_projects=all_projects,
    ))


@bp.get("/<id>/wait")
async def wait_operation(id: str):
    timeout = int(request.args.get("timeout", 60))
    public = "public" in request.args
    return jsonify(await _ctrl().wait_operation(id=id, timeout=timeout, public=public))


@bp.get("/<id>/websocket")
async def operation_websocket(id: str):
    return jsonify({"error": "operation websocket requires WebSocket handling"}), 501


@bp.get("/<id>")
async def operation_info(id: str):
    return jsonify(await _ctrl().operation_info(id=id))


@bp.delete("/<id>")
async def cancel_operation(id: str):
    await _ctrl().cancel_operation(id=id)
    return "", 200
