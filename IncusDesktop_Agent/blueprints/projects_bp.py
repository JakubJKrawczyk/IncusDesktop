# blueprints/projects_bp.py
from flask import Blueprint, current_app, jsonify, request

from controllers.incus.projects import ProjectsController


bp = Blueprint("projects", __name__, url_prefix="/projects")


def _ctrl() -> ProjectsController:
    return ProjectsController(current_app.extensions["incus"])


@bp.get("")
async def list_projects():
    recursion = int(request.args.get("recursion", 0))
    filter_ = request.args.get("filter")
    return jsonify(await _ctrl().list_projects(recursion=recursion, filter=filter_))


@bp.post("")
async def create_project():
    body = request.get_json(force=True)
    await _ctrl().create_project(body=body)
    return "", 200


@bp.get("/<name>")
async def project_info(name: str):
    return jsonify(await _ctrl().project_info(name=name))


@bp.put("/<name>")
async def update_project(name: str):
    body = request.get_json(force=True)
    await _ctrl().update_project(name=name, body=body)
    return "", 200


@bp.patch("/<name>")
async def patch_project(name: str):
    body = request.get_json(force=True)
    await _ctrl().patch_project(name=name, body=body)
    return "", 204


@bp.post("/<name>")
async def rename_project(name: str):
    body = request.get_json(force=True)
    return jsonify(await _ctrl().rename_project(name=name, new_name=body["name"])), 202


@bp.delete("/<name>")
async def delete_project(name: str):
    await _ctrl().delete_project(name=name)
    return "", 200


@bp.get("/<name>/access")
async def project_access(name: str):
    return jsonify(await _ctrl().project_access(name=name))


@bp.get("/<name>/state")
async def project_state(name: str):
    return jsonify(await _ctrl().project_state(name=name))
