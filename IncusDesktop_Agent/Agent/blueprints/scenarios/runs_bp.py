from flask import Blueprint, jsonify

from Agent.controllers.agent.scenarios.runs import RunsController


bp = Blueprint("scenarios_runs", __name__, url_prefix="/scenarios/runs")


def _ctrl() -> RunsController:
    return RunsController()


@bp.get("")
async def list_runs():
    runs = await _ctrl().list_runs()
    return jsonify([r.model_dump(mode="json") for r in runs])


@bp.get("/<run_id>")
async def get_run(run_id: str):
    run = await _ctrl().get_run(run_id)
    if run is None:
        return jsonify({"error": "run not found"}), 404
    return jsonify(run.model_dump(mode="json"))


@bp.delete("/<run_id>")
async def delete_run(run_id: str):
    deleted = await _ctrl().delete_run(run_id)
    if not deleted:
        return jsonify({"error": "run not found"}), 404
    return "", 204
