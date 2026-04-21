# blueprints/instances_snapshots_bp.py
from flask import Blueprint, current_app, jsonify, request

from controllers.incus.instances_snapshots import InstancesSnapshotsController


bp = Blueprint("instances_snapshots", __name__, url_prefix="/instances")


def _ctrl() -> InstancesSnapshotsController:
    return InstancesSnapshotsController(current_app.extensions["incus"])


@bp.get("/<name>/snapshots")
async def list_snapshots(name: str):
    project = request.args.get("project", "default")
    recursion = int(request.args.get("recursion", 0))
    return jsonify(await _ctrl().list_snapshots(name=name, recursion=recursion, project=project))


@bp.post("/<name>/snapshots")
async def create_snapshot(name: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    return jsonify(await _ctrl().create_snapshot(name=name, body=body, project=project)), 202


@bp.get("/<name>/snapshots/<snapshot>")
async def snapshot_info(name: str, snapshot: str):
    project = request.args.get("project", "default")
    return jsonify(await _ctrl().snapshot_info(name=name, snapshot=snapshot, project=project))


@bp.put("/<name>/snapshots/<snapshot>")
async def update_snapshot(name: str, snapshot: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    return jsonify(await _ctrl().update_snapshot(name=name, snapshot=snapshot, body=body, project=project)), 202


@bp.patch("/<name>/snapshots/<snapshot>")
async def patch_snapshot(name: str, snapshot: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().patch_snapshot(name=name, snapshot=snapshot, body=body, project=project)
    return "", 204


@bp.post("/<name>/snapshots/<snapshot>")
async def rename_snapshot(name: str, snapshot: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    return jsonify(await _ctrl().rename_snapshot(
        name=name, snapshot=snapshot, new_name=body["name"], project=project,
    )), 202


@bp.delete("/<name>/snapshots/<snapshot>")
async def delete_snapshot(name: str, snapshot: str):
    project = request.args.get("project", "default")
    return jsonify(await _ctrl().delete_snapshot(name=name, snapshot=snapshot, project=project)), 202
