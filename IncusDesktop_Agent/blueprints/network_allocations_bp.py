# blueprints/network_allocations_bp.py
from flask import Blueprint, current_app, jsonify, request

from controllers.incus.network_allocations import NetworkAllocationsController


bp = Blueprint("network_allocations", __name__, url_prefix="/network-allocations")


def _ctrl() -> NetworkAllocationsController:
    return NetworkAllocationsController(current_app.extensions["incus"])


@bp.get("")
async def list_allocations():
    project = request.args.get("project", "default")
    all_projects = request.args.get("all-projects") == "true"
    return jsonify(await _ctrl().list_allocations(project=project, all_projects=all_projects))
