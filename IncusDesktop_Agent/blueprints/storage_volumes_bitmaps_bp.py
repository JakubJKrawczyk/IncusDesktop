# blueprints/storage_volumes_bitmaps_bp.py
from flask import Blueprint, current_app, jsonify, request

from controllers.incus.storage_volumes_bitmaps import StorageVolumesBitmapsController


bp = Blueprint("storage_volumes_bitmaps", __name__, url_prefix="/storage-pools")


def _ctrl() -> StorageVolumesBitmapsController:
    return StorageVolumesBitmapsController(current_app.extensions["incus"])


@bp.get("/<pool>/volumes/<type>/<volume>/bitmaps")
async def list_bitmaps(pool: str, type: str, volume: str):
    project = request.args.get("project", "default")
    recursion = int(request.args.get("recursion", 0))
    return jsonify(await _ctrl().list_bitmaps(pool=pool, type=type, volume=volume, recursion=recursion, project=project))


@bp.post("/<pool>/volumes/<type>/<volume>/bitmaps")
async def create_bitmap(pool: str, type: str, volume: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    return jsonify(await _ctrl().create_bitmap(pool=pool, type=type, volume=volume, body=body, project=project)), 202


@bp.delete("/<pool>/volumes/<type>/<volume>/bitmaps/<bitmap>")
async def delete_bitmap(pool: str, type: str, volume: str, bitmap: str):
    project = request.args.get("project", "default")
    return jsonify(await _ctrl().delete_bitmap(
        pool=pool, type=type, volume=volume, bitmap=bitmap, project=project,
    )), 202
