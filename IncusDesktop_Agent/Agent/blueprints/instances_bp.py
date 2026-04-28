# blueprints/instances_bp.py
from flask import Blueprint, current_app, jsonify, request

from Agent.controllers.incus.instances import InstancesController


bp = Blueprint("instances", __name__, url_prefix="/instances")


def _ctrl() -> InstancesController:
    return InstancesController(current_app.extensions["incus"])


@bp.get("")
async def list_instances():
    project = request.args.get("project", "default")
    filter_ = request.args.get("filter")
    return jsonify(await _ctrl().list_instances(project=project, filter=filter_))


@bp.post("")
async def create_instance():
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    return jsonify(await _ctrl().create_instance(body=body, project=project)), 202


@bp.put("")
async def bulk_update_instances():
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    return jsonify(await _ctrl().bulk_update_instances(body=body, project=project)), 202


@bp.get("/<name>")
async def instance_info(name: str):
    project = request.args.get("project", "default")
    return jsonify(await _ctrl().instance_info(name=name, project=project))


@bp.put("/<name>")
async def update_instance(name: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    return jsonify(await _ctrl().update_instance(name=name, body=body, project=project)), 202


@bp.patch("/<name>")
async def patch_instance(name: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().patch_instance(name=name, body=body, project=project)
    return "", 204


@bp.post("/<name>")
async def rename_instance(name: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    return jsonify(await _ctrl().rename_instance(
        name=name, new_name=body["name"], project=project,
    )), 202


@bp.delete("/<name>")
async def delete_instance(name: str):
    project = request.args.get("project", "default")
    return jsonify(await _ctrl().delete_instance(name=name, project=project)), 202


@bp.get("/<name>/access")
async def instance_access(name: str):
    project = request.args.get("project", "default")
    return jsonify(await _ctrl().instance_access(name=name, project=project))


@bp.get("/<name>/state")
async def instance_state(name: str):
    project = request.args.get("project", "default")
    return jsonify(await _ctrl().instance_state(name=name, project=project))


@bp.put("/<name>/state")
async def set_instance_state(name: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    return jsonify(await _ctrl().set_instance_state(
        name=name,
        action=body["action"],
        timeout=body.get("timeout", 30),
        force=body.get("force", False),
        stateful=body.get("stateful", False),
        project=project,
    )), 202


@bp.post("/<name>/rebuild")
async def rebuild_instance(name: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    return jsonify(await _ctrl().rebuild_instance(
        name=name, source=body["source"], project=project,
    )), 202
