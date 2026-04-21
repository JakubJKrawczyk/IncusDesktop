# blueprints/instances_metadata_bp.py
from flask import Blueprint, current_app, jsonify, request, Response

from controllers.incus.instances_metadata import InstancesMetadataController


bp = Blueprint("instances_metadata", __name__, url_prefix="/instances")


def _ctrl() -> InstancesMetadataController:
    return InstancesMetadataController(current_app.extensions["incus"])


@bp.get("/<name>/metadata")
async def get_metadata(name: str):
    project = request.args.get("project", "default")
    return jsonify(await _ctrl().get_metadata(name=name, project=project))


@bp.put("/<name>/metadata")
async def update_metadata(name: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().update_metadata(name=name, body=body, project=project)
    return "", 204


@bp.patch("/<name>/metadata")
async def patch_metadata(name: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().patch_metadata(name=name, body=body, project=project)
    return "", 204


@bp.get("/<name>/metadata/templates")
async def templates_get(name: str):
    project = request.args.get("project", "default")
    path = request.args.get("path")
    if path:
        data = await _ctrl().get_template(name=name, path=path, project=project)
        return Response(data, mimetype="application/octet-stream")
    return jsonify(await _ctrl().list_templates(name=name, project=project))


@bp.post("/<name>/metadata/templates")
async def put_template(name: str):
    project = request.args.get("project", "default")
    path = request.args["path"]
    content = request.get_data()
    await _ctrl().put_template(name=name, path=path, content=content, project=project)
    return "", 204


@bp.delete("/<name>/metadata/templates")
async def delete_template(name: str):
    project = request.args.get("project", "default")
    path = request.args["path"]
    await _ctrl().delete_template(name=name, path=path, project=project)
    return "", 204
