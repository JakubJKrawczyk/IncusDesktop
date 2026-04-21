# blueprints/instances_exec_bp.py
from flask import Blueprint, current_app, jsonify, request, Response

from controllers.instances_exec import InstancesExecController


bp = Blueprint("instances_exec", __name__, url_prefix="/instances")


def _ctrl() -> InstancesExecController:
    return InstancesExecController(current_app.extensions["incus"])


# ─── EXEC ──────────────────────────────────────────────────────────

# POST /instances/<name>/exec
@bp.post("/<name>/exec")
def exec_command(name: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    return jsonify(_ctrl().exec_command(name=name, body=body, project=project)), 202


# ─── CONSOLE ───────────────────────────────────────────────────────

# POST /instances/<name>/console
@bp.post("/<name>/console")
def console_attach(name: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    return jsonify(_ctrl().console_attach(name=name, body=body, project=project)), 202


# GET /instances/<name>/console  (raw log)
@bp.get("/<name>/console")
def get_console_log(name: str):
    project = request.args.get("project", "default")
    data = _ctrl().get_console_log(name=name, project=project)
    return Response(data, mimetype="application/octet-stream")


# DELETE /instances/<name>/console
@bp.delete("/<name>/console")
def clear_console_log(name: str):
    project = request.args.get("project", "default")
    _ctrl().clear_console_log(name=name, project=project)
    return "", 204


# ─── LOGS ──────────────────────────────────────────────────────────

# GET /instances/<name>/logs
@bp.get("/<name>/logs")
def list_logs(name: str):
    project = request.args.get("project", "default")
    return jsonify(_ctrl().list_logs(name=name, project=project))


# GET /instances/<name>/logs/<filename>  (raw)
@bp.get("/<name>/logs/<filename>")
def get_log(name: str, filename: str):
    project = request.args.get("project", "default")
    data = _ctrl().get_log(name=name, filename=filename, project=project)
    return Response(data, mimetype="application/octet-stream")


# DELETE /instances/<name>/logs/<filename>
@bp.delete("/<name>/logs/<filename>")
def delete_log(name: str, filename: str):
    project = request.args.get("project", "default")
    _ctrl().delete_log(name=name, filename=filename, project=project)
    return "", 204


# ─── EXEC OUTPUT ───────────────────────────────────────────────────

# GET /instances/<name>/logs/exec-output
@bp.get("/<name>/logs/exec-output")
def list_exec_outputs(name: str):
    project = request.args.get("project", "default")
    return jsonify(_ctrl().list_exec_outputs(name=name, project=project))


# GET /instances/<name>/logs/exec-output/<filename>  (raw)
@bp.get("/<name>/logs/exec-output/<filename>")
def get_exec_output(name: str, filename: str):
    project = request.args.get("project", "default")
    data = _ctrl().get_exec_output(name=name, filename=filename, project=project)
    return Response(data, mimetype="application/octet-stream")


# DELETE /instances/<name>/logs/exec-output/<filename>
@bp.delete("/<name>/logs/exec-output/<filename>")
def delete_exec_output(name: str, filename: str):
    project = request.args.get("project", "default")
    _ctrl().delete_exec_output(name=name, filename=filename, project=project)
    return "", 204