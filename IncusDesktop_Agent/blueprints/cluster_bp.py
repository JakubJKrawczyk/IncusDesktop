# blueprints/cluster_bp.py
from flask import Blueprint, current_app, jsonify, request

from controllers.incus.cluster import ClusterController


bp = Blueprint("cluster", __name__, url_prefix="/cluster")


def _ctrl() -> ClusterController:
    return ClusterController(current_app.extensions["incus"])


@bp.get("")
async def cluster_info():
    return jsonify(await _ctrl().cluster_info())


@bp.put("")
async def update_cluster():
    body = request.get_json(force=True)
    return jsonify(await _ctrl().update_cluster(body=body)), 202


@bp.put("/certificate")
async def cluster_certificate():
    body = request.get_json(force=True)
    await _ctrl().cluster_certificate(body=body)
    return "", 200


# ─── Groups ────────────────────────────────────────────────────────────

@bp.get("/groups")
async def list_groups():
    recursion = int(request.args.get("recursion", 0))
    return jsonify(await _ctrl().list_groups(recursion=recursion))


@bp.post("/groups")
async def create_group():
    body = request.get_json(force=True)
    await _ctrl().create_group(body=body)
    return "", 200


@bp.get("/groups/<name>")
async def group_info(name: str):
    return jsonify(await _ctrl().group_info(name=name))


@bp.put("/groups/<name>")
async def update_group(name: str):
    body = request.get_json(force=True)
    await _ctrl().update_group(name=name, body=body)
    return "", 200


@bp.patch("/groups/<name>")
async def patch_group(name: str):
    body = request.get_json(force=True)
    await _ctrl().patch_group(name=name, body=body)
    return "", 204


@bp.post("/groups/<name>")
async def rename_group(name: str):
    body = request.get_json(force=True)
    await _ctrl().rename_group(name=name, new_name=body["name"])
    return "", 200


@bp.delete("/groups/<name>")
async def delete_group(name: str):
    await _ctrl().delete_group(name=name)
    return "", 200


# ─── Members ───────────────────────────────────────────────────────────

@bp.get("/members")
async def list_members():
    recursion = int(request.args.get("recursion", 0))
    return jsonify(await _ctrl().list_members(recursion=recursion))


@bp.post("/members")
async def request_join_token():
    body = request.get_json(force=True)
    return jsonify(await _ctrl().request_join_token(body=body)), 202


@bp.get("/members/<name>/state")
async def member_state(name: str):
    return jsonify(await _ctrl().member_state(name=name))


@bp.post("/members/<name>/state")
async def member_state_action(name: str):
    body = request.get_json(force=True)
    return jsonify(await _ctrl().member_state_action(name=name, body=body)), 202


@bp.get("/members/<name>")
async def member_info(name: str):
    return jsonify(await _ctrl().member_info(name=name))


@bp.put("/members/<name>")
async def update_member(name: str):
    body = request.get_json(force=True)
    await _ctrl().update_member(name=name, body=body)
    return "", 200


@bp.patch("/members/<name>")
async def patch_member(name: str):
    body = request.get_json(force=True)
    await _ctrl().patch_member(name=name, body=body)
    return "", 204


@bp.post("/members/<name>")
async def rename_member(name: str):
    body = request.get_json(force=True)
    await _ctrl().rename_member(name=name, new_name=body["name"])
    return "", 200


@bp.delete("/members/<name>")
async def delete_member(name: str):
    force = request.args.get("force") == "1"
    await _ctrl().delete_member(name=name, force=force)
    return "", 200
