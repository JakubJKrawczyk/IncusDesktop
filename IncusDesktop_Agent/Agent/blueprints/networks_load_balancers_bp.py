# blueprints/networks_load_balancers_bp.py
from flask import Blueprint, current_app, jsonify, request

from Agent.controllers.incus.networks_load_balancers import NetworksLoadBalancersController


bp = Blueprint("networks_load_balancers", __name__, url_prefix="/networks")


def _ctrl() -> NetworksLoadBalancersController:
    return NetworksLoadBalancersController(current_app.extensions["incus"])


@bp.get("/<network>/load-balancers")
async def list_load_balancers(network: str):
    project = request.args.get("project", "default")
    recursion = int(request.args.get("recursion", 0))
    return jsonify(await _ctrl().list_load_balancers(network=network, recursion=recursion, project=project))


@bp.post("/<network>/load-balancers")
async def create_load_balancer(network: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().create_load_balancer(network=network, body=body, project=project)
    return "", 200


@bp.get("/<network>/load-balancers/<listen_address>/state")
async def load_balancer_state(network: str, listen_address: str):
    project = request.args.get("project", "default")
    return jsonify(await _ctrl().load_balancer_state(network=network, listen_address=listen_address, project=project))


@bp.get("/<network>/load-balancers/<listen_address>")
async def load_balancer_info(network: str, listen_address: str):
    project = request.args.get("project", "default")
    return jsonify(await _ctrl().load_balancer_info(network=network, listen_address=listen_address, project=project))


@bp.put("/<network>/load-balancers/<listen_address>")
async def update_load_balancer(network: str, listen_address: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().update_load_balancer(network=network, listen_address=listen_address, body=body, project=project)
    return "", 200


@bp.patch("/<network>/load-balancers/<listen_address>")
async def patch_load_balancer(network: str, listen_address: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().patch_load_balancer(network=network, listen_address=listen_address, body=body, project=project)
    return "", 204


@bp.delete("/<network>/load-balancers/<listen_address>")
async def delete_load_balancer(network: str, listen_address: str):
    project = request.args.get("project", "default")
    await _ctrl().delete_load_balancer(network=network, listen_address=listen_address, project=project)
    return "", 200
