# blueprints/network_acls_bp.py
from flask import Blueprint, current_app, jsonify, request, Response

from controllers.incus.network_acls import NetworkACLsController


bp = Blueprint("network_acls", __name__, url_prefix="/network-acls")


def _ctrl() -> NetworkACLsController:
    return NetworkACLsController(current_app.extensions["incus"])


@bp.get("")
async def list_acls():
    project = request.args.get("project", "default")
    recursion = int(request.args.get("recursion", 0))
    return jsonify(await _ctrl().list_acls(recursion=recursion, project=project))


@bp.post("")
async def create_acl():
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().create_acl(body=body, project=project)
    return "", 200


@bp.get("/<name>/log")
async def acl_log(name: str):
    project = request.args.get("project", "default")
    data = await _ctrl().acl_log(name=name, project=project)
    return Response(data, mimetype="text/plain")


@bp.get("/<name>")
async def acl_info(name: str):
    project = request.args.get("project", "default")
    return jsonify(await _ctrl().acl_info(name=name, project=project))


@bp.put("/<name>")
async def update_acl(name: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().update_acl(name=name, body=body, project=project)
    return "", 200


@bp.patch("/<name>")
async def patch_acl(name: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().patch_acl(name=name, body=body, project=project)
    return "", 204


@bp.post("/<name>")
async def rename_acl(name: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().rename_acl(name=name, new_name=body["name"], project=project)
    return "", 200


@bp.delete("/<name>")
async def delete_acl(name: str):
    project = request.args.get("project", "default")
    await _ctrl().delete_acl(name=name, project=project)
    return "", 200
