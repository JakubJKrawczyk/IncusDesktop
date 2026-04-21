# blueprints/networks_bp.py
from flask import Blueprint, current_app, jsonify, request

from controllers.incus.networks import NetworksController


bp = Blueprint("networks", __name__, url_prefix="/networks")


def _ctrl() -> NetworksController:
    return NetworksController(current_app.extensions["incus"])


@bp.get("")
async def list_networks():
    project = request.args.get("project", "default")
    recursion = int(request.args.get("recursion", 0))
    all_projects = request.args.get("all-projects") == "true"
    return jsonify(await _ctrl().list_networks(
        recursion=recursion, project=project, all_projects=all_projects,
    ))


@bp.post("")
async def create_network():
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().create_network(body=body, project=project)
    return "", 200


@bp.get("/<name>/leases")
async def network_leases(name: str):
    project = request.args.get("project", "default")
    return jsonify(await _ctrl().network_leases(name=name, project=project))


@bp.get("/<name>/state")
async def network_state(name: str):
    project = request.args.get("project", "default")
    return jsonify(await _ctrl().network_state(name=name, project=project))


@bp.get("/<name>")
async def network_info(name: str):
    project = request.args.get("project", "default")
    return jsonify(await _ctrl().network_info(name=name, project=project))


@bp.put("/<name>")
async def update_network(name: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().update_network(name=name, body=body, project=project)
    return "", 200


@bp.patch("/<name>")
async def patch_network(name: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().patch_network(name=name, body=body, project=project)
    return "", 204


@bp.post("/<name>")
async def rename_network(name: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().rename_network(name=name, new_name=body["name"], project=project)
    return "", 200


@bp.delete("/<name>")
async def delete_network(name: str):
    project = request.args.get("project", "default")
    await _ctrl().delete_network(name=name, project=project)
    return "", 200
