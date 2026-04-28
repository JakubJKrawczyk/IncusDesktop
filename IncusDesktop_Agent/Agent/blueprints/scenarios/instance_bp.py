from flask import Blueprint, current_app, jsonify, request

from Agent.controllers.agent.scenarios.instance_config import InstanceConfigScenarios
from Agent.controllers.agent.scenarios.instance_data import InstanceDataScenarios
from Agent.controllers.agent.scenarios.instance_lifecycle import InstanceLifecycleScenarios
from Agent.models.scenarios.instance import (
    AttachNetworkSpec,
    AttachVolumeSpec,
    BackupExportSpec,
    CloneSpec,
    DecommissionSpec,
    ExposePortSpec,
    ProvisionSpec,
    ResetToSnapshotSpec,
    ResourceUpdateSpec,
    RestartSpec,
    RestoreFromBackupSpec,
    RunCommandSpec,
    SnapshotSpec,
)
from Agent.models.scenarios.runs import ScenarioRun, StepStatus


bp = Blueprint("scenarios_instance", __name__, url_prefix="/scenarios/instance")


def _client():
    return current_app.extensions["incus"]


def _serialize(run: ScenarioRun) -> tuple:
    status = 200 if run.status == StepStatus.DONE else 500
    return jsonify(run.model_dump(mode="json")), status


# ─── Lifecycle ─────────────────────────────────────────────────────────────

@bp.post("/provision")
async def provision():
    spec = ProvisionSpec(**request.get_json(force=True))
    run = await InstanceLifecycleScenarios(_client()).provision(spec)
    return _serialize(run)


@bp.post("/clone")
async def clone():
    spec = CloneSpec(**request.get_json(force=True))
    run = await InstanceLifecycleScenarios(_client()).clone(spec)
    return _serialize(run)


@bp.post("/decommission")
async def decommission():
    spec = DecommissionSpec(**request.get_json(force=True))
    run = await InstanceLifecycleScenarios(_client()).decommission(spec)
    return _serialize(run)


@bp.post("/reset-to-snapshot")
async def reset_to_snapshot():
    spec = ResetToSnapshotSpec(**request.get_json(force=True))
    run = await InstanceLifecycleScenarios(_client()).reset_to_snapshot(spec)
    return _serialize(run)


@bp.post("/restart")
async def restart():
    spec = RestartSpec(**request.get_json(force=True))
    run = await InstanceLifecycleScenarios(_client()).restart(spec)
    return _serialize(run)


# ─── Config ────────────────────────────────────────────────────────────────

@bp.patch("/<name>/resources")
async def update_resources(name: str):
    payload = request.get_json(force=True)
    payload["name"] = name
    spec = ResourceUpdateSpec(**payload)
    run = await InstanceConfigScenarios(_client()).update_resources(spec)
    return _serialize(run)


@bp.post("/<name>/attach-volume")
async def attach_volume(name: str):
    payload = request.get_json(force=True)
    payload["instance"] = name
    spec = AttachVolumeSpec(**payload)
    run = await InstanceConfigScenarios(_client()).attach_volume(spec)
    return _serialize(run)


@bp.post("/<name>/attach-network")
async def attach_network(name: str):
    payload = request.get_json(force=True)
    payload["instance"] = name
    spec = AttachNetworkSpec(**payload)
    run = await InstanceConfigScenarios(_client()).attach_network(spec)
    return _serialize(run)


@bp.post("/<name>/expose-port")
async def expose_port(name: str):
    payload = request.get_json(force=True)
    payload["instance"] = name
    spec = ExposePortSpec(**payload)
    run = await InstanceConfigScenarios(_client()).expose_port(spec)
    return _serialize(run)


@bp.post("/<name>/run-command")
async def run_command(name: str):
    payload = request.get_json(force=True)
    payload["instance"] = name
    spec = RunCommandSpec(**payload)
    run = await InstanceConfigScenarios(_client()).run_command(spec)
    return _serialize(run)


# ─── Data (snapshots / backups) ────────────────────────────────────────────

@bp.post("/<name>/snapshot")
async def snapshot(name: str):
    payload = request.get_json(silent=True) or {}
    payload["instance"] = name
    spec = SnapshotSpec(**payload)
    run = await InstanceDataScenarios(_client()).snapshot(spec)
    return _serialize(run)


@bp.post("/<name>/backup-export")
async def backup_export(name: str):
    payload = request.get_json(silent=True) or {}
    payload["instance"] = name
    spec = BackupExportSpec(**payload)
    run = await InstanceDataScenarios(_client()).backup_export(spec)
    return _serialize(run)


@bp.post("/restore-from-backup")
async def restore_from_backup():
    spec = RestoreFromBackupSpec(**request.get_json(force=True))
    run = await InstanceDataScenarios(_client()).restore_from_backup(spec)
    return _serialize(run)
