# blueprints/storage_pools_bp.py
from flask import Blueprint, current_app, jsonify, request

from Agent.controllers.incus.storage_pools import StoragePoolsController


bp = Blueprint("storage_pools", __name__, url_prefix="/storage-pools")


def _ctrl() -> StoragePoolsController:
    return StoragePoolsController(current_app.extensions["incus"])


@bp.get("")
async def list_pools():
    recursion = int(request.args.get("recursion", 0))
    return jsonify(await _ctrl().list_pools(recursion=recursion))


@bp.post("")
async def create_pool():
    body = request.get_json(force=True)
    await _ctrl().create_pool(body=body)
    return "", 200


@bp.get("/<name>/resources")
async def pool_resources(name: str):
    return jsonify(await _ctrl().pool_resources(name=name))


@bp.get("/<name>")
async def pool_info(name: str):
    return jsonify(await _ctrl().pool_info(name=name))


@bp.put("/<name>")
async def update_pool(name: str):
    body = request.get_json(force=True)
    await _ctrl().update_pool(name=name, body=body)
    return "", 200


@bp.patch("/<name>")
async def patch_pool(name: str):
    body = request.get_json(force=True)
    await _ctrl().patch_pool(name=name, body=body)
    return "", 204


@bp.delete("/<name>")
async def delete_pool(name: str):
    await _ctrl().delete_pool(name=name)
    return "", 200
