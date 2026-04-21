# blueprints/storage_buckets_keys_bp.py
from flask import Blueprint, current_app, jsonify, request

from controllers.incus.storage_buckets_keys import StorageBucketsKeysController


bp = Blueprint("storage_buckets_keys", __name__, url_prefix="/storage-pools")


def _ctrl() -> StorageBucketsKeysController:
    return StorageBucketsKeysController(current_app.extensions["incus"])


@bp.get("/<pool>/buckets/<bucket>/keys")
async def list_keys(pool: str, bucket: str):
    project = request.args.get("project", "default")
    recursion = int(request.args.get("recursion", 0))
    return jsonify(await _ctrl().list_keys(pool=pool, bucket=bucket, recursion=recursion, project=project))


@bp.post("/<pool>/buckets/<bucket>/keys")
async def create_key(pool: str, bucket: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().create_key(pool=pool, bucket=bucket, body=body, project=project)
    return "", 200


@bp.get("/<pool>/buckets/<bucket>/keys/<key>")
async def key_info(pool: str, bucket: str, key: str):
    project = request.args.get("project", "default")
    return jsonify(await _ctrl().key_info(pool=pool, bucket=bucket, key=key, project=project))


@bp.put("/<pool>/buckets/<bucket>/keys/<key>")
async def update_key(pool: str, bucket: str, key: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().update_key(pool=pool, bucket=bucket, key=key, body=body, project=project)
    return "", 200


@bp.patch("/<pool>/buckets/<bucket>/keys/<key>")
async def patch_key(pool: str, bucket: str, key: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().patch_key(pool=pool, bucket=bucket, key=key, body=body, project=project)
    return "", 204


@bp.delete("/<pool>/buckets/<bucket>/keys/<key>")
async def delete_key(pool: str, bucket: str, key: str):
    project = request.args.get("project", "default")
    await _ctrl().delete_key(pool=pool, bucket=bucket, key=key, project=project)
    return "", 200
