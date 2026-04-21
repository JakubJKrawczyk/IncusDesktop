# blueprints/images_bp.py
from flask import Blueprint, current_app, jsonify, request, Response

from controllers.incus.images import ImagesController


bp = Blueprint("images", __name__, url_prefix="/images")


def _ctrl() -> ImagesController:
    return ImagesController(current_app.extensions["incus"])


def _extract_incus_headers() -> dict:
    return {k: v for k, v in request.headers.items() if k.lower().startswith("x-incus-")}


# ─── Aliases (statyczne przed /<fingerprint>) ──────────────────────────

@bp.get("/aliases")
async def list_aliases():
    project = request.args.get("project", "default")
    recursion = int(request.args.get("recursion", 0))
    return jsonify(await _ctrl().list_aliases(recursion=recursion, project=project))


@bp.post("/aliases")
async def create_alias():
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().create_alias(body=body, project=project)
    return "", 200


@bp.get("/aliases/<name>")
async def alias_info(name: str):
    project = request.args.get("project", "default")
    public = "public" in request.args
    return jsonify(await _ctrl().alias_info(name=name, public=public, project=project))


@bp.put("/aliases/<name>")
async def update_alias(name: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().update_alias(name=name, body=body, project=project)
    return "", 200


@bp.patch("/aliases/<name>")
async def patch_alias(name: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().patch_alias(name=name, body=body, project=project)
    return "", 204


@bp.post("/aliases/<name>")
async def rename_alias(name: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().rename_alias(name=name, new_name=body["name"], project=project)
    return "", 200


@bp.delete("/aliases/<name>")
async def delete_alias(name: str):
    project = request.args.get("project", "default")
    await _ctrl().delete_alias(name=name, project=project)
    return "", 200


# ─── Images ────────────────────────────────────────────────────────────

@bp.get("")
async def list_images():
    project = request.args.get("project", "default")
    recursion = int(request.args.get("recursion", 0))
    public = "public" in request.args
    filter_ = request.args.get("filter")
    all_projects = request.args.get("all-projects") == "true"
    return jsonify(await _ctrl().list_images(
        recursion=recursion, public=public, project=project,
        filter=filter_, all_projects=all_projects,
    ))


@bp.post("")
async def create_or_upload_image():
    project = request.args.get("project", "default")
    content_type = (request.content_type or "").lower()
    if content_type.startswith("application/json"):
        body = request.get_json(force=True)
        return jsonify(await _ctrl().create_image(body=body, project=project)), 202
    headers = _extract_incus_headers()
    return jsonify(await _ctrl().upload_image(
        content=request.get_data(),
        headers=headers,
        project=project,
    )), 202


@bp.get("/<fingerprint>")
async def image_info(fingerprint: str):
    project = request.args.get("project", "default")
    public = "public" in request.args
    return jsonify(await _ctrl().image_info(fingerprint=fingerprint, public=public, project=project))


@bp.put("/<fingerprint>")
async def update_image(fingerprint: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().update_image(fingerprint=fingerprint, body=body, project=project)
    return "", 200


@bp.patch("/<fingerprint>")
async def patch_image(fingerprint: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    await _ctrl().patch_image(fingerprint=fingerprint, body=body, project=project)
    return "", 204


@bp.delete("/<fingerprint>")
async def delete_image(fingerprint: str):
    project = request.args.get("project", "default")
    return jsonify(await _ctrl().delete_image(fingerprint=fingerprint, project=project)), 202


@bp.get("/<fingerprint>/export")
async def export_image(fingerprint: str):
    project = request.args.get("project", "default")
    public = "public" in request.args
    data = await _ctrl().export_image(fingerprint=fingerprint, public=public, project=project)
    return Response(data, mimetype="application/octet-stream")


@bp.post("/<fingerprint>/export")
async def push_export_image(fingerprint: str):
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    return jsonify(await _ctrl().push_export_image(fingerprint=fingerprint, body=body, project=project)), 202


@bp.post("/<fingerprint>/refresh")
async def refresh_image(fingerprint: str):
    project = request.args.get("project", "default")
    return jsonify(await _ctrl().refresh_image(fingerprint=fingerprint, project=project)), 202


@bp.post("/<fingerprint>/secret")
async def create_image_secret(fingerprint: str):
    project = request.args.get("project", "default")
    return jsonify(await _ctrl().create_image_secret(fingerprint=fingerprint, project=project)), 202
