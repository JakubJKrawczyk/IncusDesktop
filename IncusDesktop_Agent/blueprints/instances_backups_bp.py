# blueprints/instances_backups_bp.py
from flask import Blueprint, current_app, jsonify, request, Response

from controllers.incus.instances_backups import InstancesBackupsController


bp = Blueprint("instances_backups", __name__, url_prefix="/instances")


def _ctrl() -> InstancesBackupsController:
    return InstancesBackupsController(current_app.extensions["incus"])


@bp.get("/<name>/backups")
async def list_backups(name: str):
    project = request.args.get("project", "default")
    recursion = int(request.args.get("recursion", 0))
    return jsonify(await _ctrl().list_backups(name=name, recursion=recursion, project=project))


@bp.post("/<name>/backups")
async def create_backup(name: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    return jsonify(await _ctrl().create_backup(name=name, body=body, project=project)), 202


@bp.get("/<name>/backups/<backup>")
async def backup_info(name: str, backup: str):
    project = request.args.get("project", "default")
    return jsonify(await _ctrl().backup_info(name=name, backup=backup, project=project))


@bp.post("/<name>/backups/<backup>")
async def rename_backup(name: str, backup: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    return jsonify(await _ctrl().rename_backup(
        name=name, backup=backup, new_name=body["name"], project=project,
    )), 202


@bp.delete("/<name>/backups/<backup>")
async def delete_backup(name: str, backup: str):
    project = request.args.get("project", "default")
    return jsonify(await _ctrl().delete_backup(name=name, backup=backup, project=project)), 202


@bp.get("/<name>/backups/<backup>/export")
async def export_backup(name: str, backup: str):
    project = request.args.get("project", "default")
    data = await _ctrl().export_backup(name=name, backup=backup, project=project)
    return Response(data, mimetype="application/octet-stream")
