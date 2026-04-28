# blueprints/storage_volumes_snapshots_bp.py
from flask import Blueprint, current_app, jsonify, request

from Agent.controllers.incus.storage_volumes_snapshots import StorageVolumesSnapshotsController


bp = Blueprint("storage_volumes_snapshots", __name__, url_prefix="/storage-pools")


def _ctrl() -> StorageVolumesSnapshotsController:
    return StorageVolumesSnapshotsController(current_app.extensions["incus"])


@bp.get("/<pool>/volumes/<type>/<volume>/snapshots")
async def list_snapshots(pool: str, type: str, volume: str):
    project = request.args.get("project", "default")
    recursion = int(request.args.get("recursion", 0))
    return jsonify(await _ctrl().list_snapshots(pool=pool, type=type, volume=volume, recursion=recursion, project=project))


@bp.post("/<pool>/volumes/<type>/<volume>/snapshots")
async def create_snapshot(pool: str, type: str, volume: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    return jsonify(await _ctrl().create_snapshot(pool=pool, type=type, volume=volume, body=body, project=project)), 202


@bp.get("/<pool>/volumes/<type>/<volume>/snapshots/<snapshot>")
async def snapshot_info(pool: str, type: str, volume: str, snapshot: str):
    project = request.args.get("project", "default")
    return jsonify(await _ctrl().snapshot_info(pool=pool, type=type, volume=volume, snapshot=snapshot, project=project))


@bp.put("/<pool>/volumes/<type>/<volume>/snapshots/<snapshot>")
async def update_snapshot(pool: str, type: str, volume: str, snapshot: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().update_snapshot(pool=pool, type=type, volume=volume, snapshot=snapshot, body=body, project=project)
    return "", 200


@bp.patch("/<pool>/volumes/<type>/<volume>/snapshots/<snapshot>")
async def patch_snapshot(pool: str, type: str, volume: str, snapshot: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().patch_snapshot(pool=pool, type=type, volume=volume, snapshot=snapshot, body=body, project=project)
    return "", 204


@bp.post("/<pool>/volumes/<type>/<volume>/snapshots/<snapshot>")
async def rename_snapshot(pool: str, type: str, volume: str, snapshot: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    return jsonify(await _ctrl().rename_snapshot(
        pool=pool, type=type, volume=volume, snapshot=snapshot, new_name=body["name"], project=project,
    )), 202


@bp.delete("/<pool>/volumes/<type>/<volume>/snapshots/<snapshot>")
async def delete_snapshot(pool: str, type: str, volume: str, snapshot: str):
    project = request.args.get("project", "default")
    return jsonify(await _ctrl().delete_snapshot(
        pool=pool, type=type, volume=volume, snapshot=snapshot, project=project,
    )), 202
