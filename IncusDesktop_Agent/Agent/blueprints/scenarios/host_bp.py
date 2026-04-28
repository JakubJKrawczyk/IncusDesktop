from flask import Blueprint, current_app, jsonify, request

from Agent.controllers.agent.scenarios.host_setup import HostSetupScenarios
from Agent.models.scenarios.host import HostBootstrapSpec, ProjectBootstrapSpec
from Agent.models.scenarios.runs import ScenarioRun, StepStatus


bp = Blueprint("scenarios_host", __name__, url_prefix="/scenarios")


def _client():
    return current_app.extensions["incus"]


def _serialize(run: ScenarioRun) -> tuple:
    status = 200 if run.status == StepStatus.DONE else 500
    return jsonify(run.model_dump(mode="json")), status


@bp.post("/host/bootstrap")
async def host_bootstrap():
    payload = request.get_json(silent=True) or {}
    spec = HostBootstrapSpec(**payload)
    run = await HostSetupScenarios(_client()).host_bootstrap(spec)
    return _serialize(run)


@bp.post("/project/bootstrap")
async def project_bootstrap():
    spec = ProjectBootstrapSpec(**request.get_json(force=True))
    run = await HostSetupScenarios(_client()).project_bootstrap(spec)
    return _serialize(run)
