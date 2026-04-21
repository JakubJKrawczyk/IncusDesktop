# blueprints/networks_forwards_bp.py
from flask import Blueprint, current_app, jsonify, request

from controllers.incus.networks_forwards import NetworksForwardsController


bp = Blueprint("networks_forwards", __name__, url_prefix="/networks")


def _ctrl() -> NetworksForwardsController:
    return NetworksForwardsController(current_app.extensions["incus"])


@bp.get("/<network>/forwards")
async def list_forwards(network: str):
    project = request.args.get("project", "default")
    recursion = int(request.args.get("recursion", 0))
    return jsonify(await _ctrl().list_forwards(network=network, recursion=recursion, project=project))


@bp.post("/<network>/forwards")
async def create_forward(network: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().create_forward(network=network, body=body, project=project)
    return "", 200


@bp.get("/<network>/forwards/<listen_address>")
async def forward_info(network: str, listen_address: str):
    project = request.args.get("project", "default")
    return jsonify(await _ctrl().forward_info(network=network, listen_address=listen_address, project=project))


@bp.put("/<network>/forwards/<listen_address>")
async def update_forward(network: str, listen_address: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().update_forward(network=network, listen_address=listen_address, body=body, project=project)
    return "", 200


@bp.patch("/<network>/forwards/<listen_address>")
async def patch_forward(network: str, listen_address: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().patch_forward(network=network, listen_address=listen_address, body=body, project=project)
    return "", 204


@bp.delete("/<network>/forwards/<listen_address>")
async def delete_forward(network: str, listen_address: str):
    project = request.args.get("project", "default")
    await _ctrl().delete_forward(network=network, listen_address=listen_address, project=project)
    return "", 200
