from dataclasses import asdict

from flask import Blueprint, jsonify

from Agent.controllers.agent.rawCommands.rawCommands import RawCommandsController


bp = Blueprint("commands", __name__, url_prefix="/command")


def _ctrl() -> RawCommandsController:
    return RawCommandsController()

@bp.get("/health_incus")
async def health_check_incus():
    result = await _ctrl().HealthCheckIncus()

    status = 200 if result.stdout.find("Active: active (running)") != -1 else 503 if result.stdout.find("Active: inactive (dead)") != -1 else 404
    response = "OK" if status == 200 else "Not OK" if status == 503 else "Incus not Found" if status == 404 else "Internal Server Error"
    return jsonify(response), status

@bp.get("/health")
async def health_check():
    return jsonify({"status": "ok"}), 200