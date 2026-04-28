# blueprints/server_bp.py
from flask import Blueprint, current_app, jsonify, request, Response

from Agent.controllers.incus.server import ServerController


bp = Blueprint("server", __name__)


def _ctrl() -> ServerController:
    return ServerController(current_app.extensions["incus"])


@bp.get("/")
async def root():
    return jsonify(await _ctrl().root())


@bp.get("/server")
async def server_info():
    public = "public" in request.args
    return jsonify(await _ctrl().server_info(public=public))


@bp.put("/server")
async def update_server():
    body = request.get_json(force=True)
    await _ctrl().update_server(body=body)
    return "", 200


@bp.patch("/server")
async def patch_server():
    body = request.get_json(force=True)
    await _ctrl().patch_server(body=body)
    return "", 204


@bp.get("/events")
async def events_stream():
    return jsonify({"error": "events stream requires WebSocket handling"}), 501


@bp.get("/resources")
async def resources():
    return jsonify(await _ctrl().resources())


@bp.get("/metrics")
async def metrics():
    project = request.args.get("project")
    data = await _ctrl().metrics(project=project)
    return Response(data, mimetype="text/plain; version=0.0.4")


@bp.get("/metadata/configuration")
async def metadata_configuration():
    return jsonify(await _ctrl().metadata_configuration())
