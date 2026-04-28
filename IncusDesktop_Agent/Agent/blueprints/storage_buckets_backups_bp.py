# blueprints/storage_buckets_backups_bp.py
from flask import Blueprint, current_app, jsonify, request, Response

from Agent.controllers.incus.storage_buckets_backups import StorageBucketsBackupsController


bp = Blueprint("storage_buckets_backups", __name__, url_prefix="/storage-pools")


def _ctrl() -> StorageBucketsBackupsController:
    return StorageBucketsBackupsController(current_app.extensions["incus"])


@bp.get("/<pool>/buckets/<bucket>/backups")
async def list_backups(pool: str, bucket: str):
    project = request.args.get("project", "default")
    recursion = int(request.args.get("recursion", 0))
    return jsonify(await _ctrl().list_backups(pool=pool, bucket=bucket, recursion=recursion, project=project))


@bp.post("/<pool>/buckets/<bucket>/backups")
async def create_backup(pool: str, bucket: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    return jsonify(await _ctrl().create_backup(pool=pool, bucket=bucket, body=body, project=project)), 202


@bp.get("/<pool>/buckets/<bucket>/backups/<backup>/export")
async def export_backup(pool: str, bucket: str, backup: str):
    project = request.args.get("project", "default")
    data = await _ctrl().export_backup(pool=pool, bucket=bucket, backup=backup, project=project)
    return Response(data, mimetype="application/octet-stream")


@bp.get("/<pool>/buckets/<bucket>/backups/<backup>")
async def backup_info(pool: str, bucket: str, backup: str):
    project = request.args.get("project", "default")
    return jsonify(await _ctrl().backup_info(pool=pool, bucket=bucket, backup=backup, project=project))


@bp.post("/<pool>/buckets/<bucket>/backups/<backup>")
async def rename_backup(pool: str, bucket: str, backup: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    return jsonify(await _ctrl().rename_backup(
        pool=pool, bucket=bucket, backup=backup, new_name=body["name"], project=project,
    )), 202


@bp.delete("/<pool>/buckets/<bucket>/backups/<backup>")
async def delete_backup(pool: str, bucket: str, backup: str):
    project = request.args.get("project", "default")
    return jsonify(await _ctrl().delete_backup(
        pool=pool, bucket=bucket, backup=backup, project=project,
    )), 202
