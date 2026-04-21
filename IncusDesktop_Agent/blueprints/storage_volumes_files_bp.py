# blueprints/storage_volumes_files_bp.py
from flask import Blueprint, current_app, request, Response

from controllers.incus.storage_volumes_files import StorageVolumesFilesController


bp = Blueprint("storage_volumes_files", __name__, url_prefix="/storage-pools")


def _ctrl() -> StorageVolumesFilesController:
    return StorageVolumesFilesController(current_app.extensions["incus"])


@bp.get("/<pool>/volumes/<type>/<volume>/files")
async def get_file(pool: str, type: str, volume: str):
    project = request.args.get("project", "default")
    path = request.args["path"]
    data, headers = await _ctrl().get_file(pool=pool, type=type, volume=volume, path=path, project=project)
    forward = {k: v for k, v in headers.items() if k.lower().startswith("x-incus-")}
    return Response(data, mimetype="application/octet-stream", headers=forward)


@bp.route("/<pool>/volumes/<type>/<volume>/files", methods=["HEAD"])
async def stat_file(pool: str, type: str, volume: str):
    project = request.args.get("project", "default")
    path = request.args["path"]
    headers = await _ctrl().stat_file(pool=pool, type=type, volume=volume, path=path, project=project)
    forward = {k: v for k, v in headers.items() if k.lower().startswith("x-incus-")}
    return Response(status=200, headers=forward)


@bp.post("/<pool>/volumes/<type>/<volume>/files")
async def put_file(pool: str, type: str, volume: str):
    project = request.args.get("project", "default")
    path = request.args["path"]
    content = request.get_data()
    type_ = request.headers.get("X-Incus-type", "file")
    write_mode = request.headers.get("X-Incus-write", "overwrite")
    uid = int(request.headers["X-Incus-uid"]) if "X-Incus-uid" in request.headers else None
    gid = int(request.headers["X-Incus-gid"]) if "X-Incus-gid" in request.headers else None
    mode = int(request.headers["X-Incus-mode"]) if "X-Incus-mode" in request.headers else None
    await _ctrl().put_file(
        pool=pool, type=type, volume=volume, path=path, content=content,
        uid=uid, gid=gid, mode=mode, type_=type_, write_mode=write_mode, project=project,
    )
    return "", 200


@bp.delete("/<pool>/volumes/<type>/<volume>/files")
async def delete_file(pool: str, type: str, volume: str):
    project = request.args.get("project", "default")
    path = request.args["path"]
    recursive = request.headers.get("X-Incus-force", "").lower() == "true"
    await _ctrl().delete_file(pool=pool, type=type, volume=volume, path=path, recursive=recursive, project=project)
    return "", 200
