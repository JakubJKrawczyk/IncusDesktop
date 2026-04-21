# blueprints/profiles_bp.py
from flask import Blueprint, current_app, jsonify, request

from controllers.incus.profiles import ProfilesController


bp = Blueprint("profiles", __name__, url_prefix="/profiles")


def _ctrl() -> ProfilesController:
    return ProfilesController(current_app.extensions["incus"])


@bp.get("")
async def list_profiles():
    project = request.args.get("project", "default")
    recursion = int(request.args.get("recursion", 0))
    filter_ = request.args.get("filter")
    return jsonify(await _ctrl().list_profiles(recursion=recursion, project=project, filter=filter_))


@bp.post("")
async def create_profile():
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().create_profile(body=body, project=project)
    return "", 200


@bp.get("/<name>")
async def profile_info(name: str):
    project = request.args.get("project", "default")
    return jsonify(await _ctrl().profile_info(name=name, project=project))


@bp.put("/<name>")
async def update_profile(name: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().update_profile(name=name, body=body, project=project)
    return "", 200


@bp.patch("/<name>")
async def patch_profile(name: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().patch_profile(name=name, body=body, project=project)
    return "", 204


@bp.post("/<name>")
async def rename_profile(name: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().rename_profile(name=name, new_name=body["name"], project=project)
    return "", 200


@bp.delete("/<name>")
async def delete_profile(name: str):
    project = request.args.get("project", "default")
    await _ctrl().delete_profile(name=name, project=project)
    return "", 200
