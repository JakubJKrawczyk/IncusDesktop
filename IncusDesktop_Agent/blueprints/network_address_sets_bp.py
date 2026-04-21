# blueprints/network_address_sets_bp.py
from flask import Blueprint, current_app, jsonify, request

from controllers.incus.network_address_sets import NetworkAddressSetsController


bp = Blueprint("network_address_sets", __name__, url_prefix="/network-address-sets")


def _ctrl() -> NetworkAddressSetsController:
    return NetworkAddressSetsController(current_app.extensions["incus"])


@bp.get("")
async def list_address_sets():
    project = request.args.get("project", "default")
    recursion = int(request.args.get("recursion", 0))
    return jsonify(await _ctrl().list_address_sets(recursion=recursion, project=project))


@bp.post("")
async def create_address_set():
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().create_address_set(body=body, project=project)
    return "", 200


@bp.get("/<name>")
async def address_set_info(name: str):
    project = request.args.get("project", "default")
    return jsonify(await _ctrl().address_set_info(name=name, project=project))


@bp.put("/<name>")
async def update_address_set(name: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().update_address_set(name=name, body=body, project=project)
    return "", 200


@bp.patch("/<name>")
async def patch_address_set(name: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().patch_address_set(name=name, body=body, project=project)
    return "", 204


@bp.post("/<name>")
async def rename_address_set(name: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().rename_address_set(name=name, new_name=body["name"], project=project)
    return "", 200


@bp.delete("/<name>")
async def delete_address_set(name: str):
    project = request.args.get("project", "default")
    await _ctrl().delete_address_set(name=name, project=project)
    return "", 200
