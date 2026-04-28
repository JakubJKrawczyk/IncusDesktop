# blueprints/storage_buckets_bp.py
from flask import Blueprint, current_app, jsonify, request

from Agent.controllers.incus.storage_buckets import StorageBucketsController


bp = Blueprint("storage_buckets", __name__, url_prefix="/storage-pools")


def _ctrl() -> StorageBucketsController:
    return StorageBucketsController(current_app.extensions["incus"])


@bp.get("/<pool>/buckets")
async def list_buckets(pool: str):
    project = request.args.get("project", "default")
    recursion = int(request.args.get("recursion", 0))
    return jsonify(await _ctrl().list_buckets(pool=pool, recursion=recursion, project=project))


@bp.post("/<pool>/buckets")
async def create_bucket(pool: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().create_bucket(pool=pool, body=body, project=project)
    return "", 200


@bp.get("/<pool>/buckets/<name>")
async def bucket_info(pool: str, name: str):
    project = request.args.get("project", "default")
    return jsonify(await _ctrl().bucket_info(pool=pool, name=name, project=project))


@bp.put("/<pool>/buckets/<name>")
async def update_bucket(pool: str, name: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().update_bucket(pool=pool, name=name, body=body, project=project)
    return "", 200


@bp.patch("/<pool>/buckets/<name>")
async def patch_bucket(pool: str, name: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().patch_bucket(pool=pool, name=name, body=body, project=project)
    return "", 204


@bp.delete("/<pool>/buckets/<name>")
async def delete_bucket(pool: str, name: str):
    project = request.args.get("project", "default")
    await _ctrl().delete_bucket(pool=pool, name=name, project=project)
    return "", 200
