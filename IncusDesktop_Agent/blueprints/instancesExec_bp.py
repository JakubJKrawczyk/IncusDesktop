# blueprints/instancesExec_bp.py
from flask import Blueprint, current_app, jsonify, request, Response

from controllers.incus.instances_exec import InstancesExecController


bp = Blueprint("instances_exec", __name__, url_prefix="/instances")


def _ctrl() -> InstancesExecController:
    return InstancesExecController(current_app.extensions["incus"])


@bp.post("/<name>/exec")
async def exec_command(name: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    return jsonify(await _ctrl().exec_command(name=name, body=body, project=project)), 202


@bp.post("/<name>/console")
async def console_attach(name: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    return jsonify(await _ctrl().console_attach(name=name, body=body, project=project)), 202


@bp.get("/<name>/console")
async def get_console_log(name: str):
    project = request.args.get("project", "default")
    data = await _ctrl().get_console_log(name=name, project=project)
    return Response(data, mimetype="application/octet-stream")


@bp.delete("/<name>/console")
async def clear_console_log(name: str):
    project = request.args.get("project", "default")
    await _ctrl().clear_console_log(name=name, project=project)
    return "", 204


@bp.get("/<name>/logs")
async def list_logs(name: str):
    project = request.args.get("project", "default")
    return jsonify(await _ctrl().list_logs(name=name, project=project))


@bp.get("/<name>/logs/<filename>")
async def get_log(name: str, filename: str):
    project = request.args.get("project", "default")
    data = await _ctrl().get_log(name=name, filename=filename, project=project)
    return Response(data, mimetype="application/octet-stream")


@bp.delete("/<name>/logs/<filename>")
async def delete_log(name: str, filename: str):
    project = request.args.get("project", "default")
    await _ctrl().delete_log(name=name, filename=filename, project=project)
    return "", 204


@bp.get("/<name>/logs/exec-output")
async def list_exec_outputs(name: str):
    project = request.args.get("project", "default")
    return jsonify(await _ctrl().list_exec_outputs(name=name, project=project))


@bp.get("/<name>/logs/exec-output/<filename>")
async def get_exec_output(name: str, filename: str):
    project = request.args.get("project", "default")
    data = await _ctrl().get_exec_output(name=name, filename=filename, project=project)
    return Response(data, mimetype="application/octet-stream")


@bp.delete("/<name>/logs/exec-output/<filename>")
async def delete_exec_output(name: str, filename: str):
    project = request.args.get("project", "default")
    await _ctrl().delete_exec_output(name=name, filename=filename, project=project)
    return "", 204
