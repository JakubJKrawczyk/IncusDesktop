# blueprints/storage_volumes_backups_bp.py
from flask import Blueprint, current_app, jsonify, request, Response

from Agent.controllers.incus.storage_volumes_backups import StorageVolumesBackupsController


bp = Blueprint("storage_volumes_backups", __name__, url_prefix="/storage-pools")


def _ctrl() -> StorageVolumesBackupsController:
    return StorageVolumesBackupsController(current_app.extensions["incus"])


@bp.get("/<pool>/volumes/<type>/<volume>/backups")
async def list_backups(pool: str, type: str, volume: str):
    project = request.args.get("project", "default")
    recursion = int(request.args.get("recursion", 0))
    return jsonify(await _ctrl().list_backups(pool=pool, type=type, volume=volume, recursion=recursion, project=project))


@bp.post("/<pool>/volumes/<type>/<volume>/backups")
async def create_backup(pool: str, type: str, volume: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    return jsonify(await _ctrl().create_backup(pool=pool, type=type, volume=volume, body=body, project=project)), 202


@bp.get("/<pool>/volumes/<type>/<volume>/backups/<backup>/export")
async def export_backup(pool: str, type: str, volume: str, backup: str):
    project = request.args.get("project", "default")
    data = await _ctrl().export_backup(pool=pool, type=type, volume=volume, backup=backup, project=project)
    return Response(data, mimetype="application/octet-stream")


@bp.get("/<pool>/volumes/<type>/<volume>/backups/<backup>")
async def backup_info(pool: str, type: str, volume: str, backup: str):
    project = request.args.get("project", "default")
    return jsonify(await _ctrl().backup_info(pool=pool, type=type, volume=volume, backup=backup, project=project))


@bp.post("/<pool>/volumes/<type>/<volume>/backups/<backup>")
async def rename_backup(pool: str, type: str, volume: str, backup: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    return jsonify(await _ctrl().rename_backup(
        pool=pool, type=type, volume=volume, backup=backup, new_name=body["name"], project=project,
    )), 202


@bp.delete("/<pool>/volumes/<type>/<volume>/backups/<backup>")
async def delete_backup(pool: str, type: str, volume: str, backup: str):
    project = request.args.get("project", "default")
    return jsonify(await _ctrl().delete_backup(
        pool=pool, type=type, volume=volume, backup=backup, project=project,
    )), 202
