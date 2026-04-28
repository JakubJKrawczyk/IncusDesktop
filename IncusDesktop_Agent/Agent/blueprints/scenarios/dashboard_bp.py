from flask import Blueprint, current_app, jsonify, request

from Agent.controllers.agent.scenarios.dashboard import DashboardScenarios
from Agent.models.scenarios.runs import ScenarioRun, StepStatus


bp = Blueprint("scenarios_dashboard", __name__, url_prefix="/scenarios")


def _client():
    return current_app.extensions["incus"]


def _serialize(run: ScenarioRun) -> tuple:
    status = 200 if run.status == StepStatus.DONE else 500
    return jsonify(run.model_dump(mode="json")), status


@bp.get("/dashboard")
async def dashboard():
    project = request.args.get("project", "default")
    run = await DashboardScenarios(_client()).dashboard(project=project)
    return _serialize(run)


@bp.get("/instance/<name>/full")
async def instance_full(name: str):
    project = request.args.get("project", "default")
    run = await DashboardScenarios(_client()).instance_full(name=name, project=project)
    return _serialize(run)
