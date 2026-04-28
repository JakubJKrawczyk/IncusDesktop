# blueprints/networks_peers_bp.py
from flask import Blueprint, current_app, jsonify, request

from Agent.controllers.incus.networks_peers import NetworksPeersController


bp = Blueprint("networks_peers", __name__, url_prefix="/networks")


def _ctrl() -> NetworksPeersController:
    return NetworksPeersController(current_app.extensions["incus"])


@bp.get("/<network>/peers")
async def list_peers(network: str):
    project = request.args.get("project", "default")
    recursion = int(request.args.get("recursion", 0))
    return jsonify(await _ctrl().list_peers(network=network, recursion=recursion, project=project))


@bp.post("/<network>/peers")
async def create_peer(network: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().create_peer(network=network, body=body, project=project)
    return "", 200


@bp.get("/<network>/peers/<peer_name>")
async def peer_info(network: str, peer_name: str):
    project = request.args.get("project", "default")
    return jsonify(await _ctrl().peer_info(network=network, peer_name=peer_name, project=project))


@bp.put("/<network>/peers/<peer_name>")
async def update_peer(network: str, peer_name: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().update_peer(network=network, peer_name=peer_name, body=body, project=project)
    return "", 200


@bp.patch("/<network>/peers/<peer_name>")
async def patch_peer(network: str, peer_name: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().patch_peer(network=network, peer_name=peer_name, body=body, project=project)
    return "", 204


@bp.delete("/<network>/peers/<peer_name>")
async def delete_peer(network: str, peer_name: str):
    project = request.args.get("project", "default")
    await _ctrl().delete_peer(network=network, peer_name=peer_name, project=project)
    return "", 200
