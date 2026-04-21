# app/controllers/instances_bp.py
from flask import Blueprint, current_app, jsonify, request

# from ..middleware.auth import require_token
from controllers.instances import InstancesController


bp = Blueprint("instances", __name__, url_prefix="/instances")
# bp.before_request(require_token)  # auth dla calej grupy


def _ctrl() -> InstancesController:
    """Wyciaga IncusRestClient z app.extensions i tworzy controller."""
    return InstancesController(current_app.extensions["incus"])


# GET /instances?project=default&filter=...
@bp.get("")
def list_instances():
    project = request.args.get("project", "default")
    filter_ = request.args.get("filter")
    return jsonify(_ctrl().list_instances(project=project, filter=filter_))


# POST /instances
@bp.post("")
def create_instance():
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    return jsonify(_ctrl().create_instance(body=body, project=project)), 202


# GET /instances/<name>
@bp.get("/<name>")
def instance_info(name: str):
    project = request.args.get("project", "default")
    return jsonify(_ctrl().instance_info(name=name, project=project))


# PUT /instances/<name>
@bp.put("/<name>")
def update_instance(name: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    return jsonify(_ctrl().update_instance(name=name, body=body, project=project)), 202


# PATCH /instances/<name>
@bp.patch("/<name>")
def patch_instance(name: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    _ctrl().patch_instance(name=name, body=body, project=project)
    return "", 204


# POST /instances/<name>  (rename)
@bp.post("/<name>")
def rename_instance(name: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    return jsonify(_ctrl().rename_instance(
        name=name, new_name=body["name"], project=project,
    )), 202


# DELETE /instances/<name>
@bp.delete("/<name>")
def delete_instance(name: str):
    project = request.args.get("project", "default")
    return jsonify(_ctrl().delete_instance(name=name, project=project)), 202


# GET /instances/<name>/access
@bp.get("/<name>/access")
def instance_access(name: str):
    project = request.args.get("project", "default")
    return jsonify(_ctrl().instance_access(name=name, project=project))


# GET /instances/<name>/state
@bp.get("/<name>/state")
def instance_state(name: str):
    project = request.args.get("project", "default")
    return jsonify(_ctrl().instance_state(name=name, project=project))


# PUT /instances/<name>/state
@bp.put("/<name>/state")
def set_instance_state(name: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    return jsonify(_ctrl().set_instance_state(
        name=name,
        action=body["action"],
        timeout=body.get("timeout", 30),
        force=body.get("force", False),
        stateful=body.get("stateful", False),
        project=project,
    )), 202


# POST /instances/<name>/rebuild
@bp.post("/<name>/rebuild")
def rebuild_instance(name: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    return jsonify(_ctrl().rebuild_instance(
        name=name, source=body["source"], project=project,
    )), 202