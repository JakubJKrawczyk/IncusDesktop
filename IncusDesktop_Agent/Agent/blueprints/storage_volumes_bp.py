# blueprints/storage_volumes_bp.py
from flask import Blueprint, current_app, jsonify, request

from Agent.controllers.incus.storage_volumes import StorageVolumesController


bp = Blueprint("storage_volumes", __name__, url_prefix="/storage-pools")


def _ctrl() -> StorageVolumesController:
    return StorageVolumesController(current_app.extensions["incus"])


def _extract_incus_headers() -> dict:
    return {k: v for k, v in request.headers.items() if k.lower().startswith("x-incus-")}


@bp.get("/<pool>/volumes")
async def list_volumes(pool: str):
    project = request.args.get("project", "default")
    recursion = int(request.args.get("recursion", 0))
    return jsonify(await _ctrl().list_volumes(pool=pool, recursion=recursion, project=project))


@bp.post("/<pool>/volumes")
async def create_volume(pool: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().create_volume(pool=pool, body=body, project=project)
    return "", 200


@bp.get("/<pool>/volumes/<type>")
async def list_volumes_by_type(pool: str, type: str):
    project = request.args.get("project", "default")
    recursion = int(request.args.get("recursion", 0))
    return jsonify(await _ctrl().list_volumes_by_type(pool=pool, type=type, recursion=recursion, project=project))


@bp.post("/<pool>/volumes/<type>")
async def create_volume_or_import(pool: str, type: str):
    project = request.args.get("project", "default")
    content_type = (request.content_type or "").lower()
    if type == "custom" and not content_type.startswith("application/json"):
        headers = _extract_incus_headers()
        return jsonify(await _ctrl().import_volume_from_backup(
            pool=pool, content=request.get_data(), headers=headers, project=project,
        )), 202
    body = request.get_json(force=True)
    await _ctrl().create_volume_by_type(pool=pool, type=type, body=body, project=project)
    return "", 200


@bp.get("/<pool>/volumes/<type>/<name>/state")
async def volume_state(pool: str, type: str, name: str):
    project = request.args.get("project", "default")
    return jsonify(await _ctrl().volume_state(pool=pool, type=type, name=name, project=project))


@bp.get("/<pool>/volumes/<type>/<name>/nbd")
async def volume_nbd(pool: str, type: str, name: str):
    return jsonify({"error": "NBD endpoint requires socket hijacking"}), 501


@bp.get("/<pool>/volumes/<type>/<name>/sftp")
async def volume_sftp(pool: str, type: str, name: str):
    return jsonify({"error": "SFTP endpoint requires HTTP upgrade"}), 501


@bp.get("/<pool>/volumes/<type>/<name>")
async def volume_info(pool: str, type: str, name: str):
    project = request.args.get("project", "default")
    return jsonify(await _ctrl().volume_info(pool=pool, type=type, name=name, project=project))


@bp.put("/<pool>/volumes/<type>/<name>")
async def update_volume(pool: str, type: str, name: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().update_volume(pool=pool, type=type, name=name, body=body, project=project)
    return "", 200


@bp.patch("/<pool>/volumes/<type>/<name>")
async def patch_volume(pool: str, type: str, name: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().patch_volume(pool=pool, type=type, name=name, body=body, project=project)
    return "", 204


@bp.post("/<pool>/volumes/<type>/<name>")
async def rename_volume(pool: str, type: str, name: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    return jsonify(await _ctrl().rename_volume(
        pool=pool, type=type, name=name, body=body, project=project,
    )), 202


@bp.delete("/<pool>/volumes/<type>/<name>")
async def delete_volume(pool: str, type: str, name: str):
    project = request.args.get("project", "default")
    await _ctrl().delete_volume(pool=pool, type=type, name=name, project=project)
    return "", 200
