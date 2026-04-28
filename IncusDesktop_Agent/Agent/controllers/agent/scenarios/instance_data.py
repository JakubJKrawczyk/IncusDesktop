from datetime import datetime, timezone
from typing import Any

from Agent.controllers.agent.scenarios import _helpers
from Agent.controllers.agent.scenarios._runner import ScenarioRunner
from Agent.controllers.incus.instances import InstancesController
from Agent.controllers.incus.instances_backups import InstancesBackupsController
from Agent.controllers.incus.instances_snapshots import InstancesSnapshotsController
from Agent.models.scenarios.instance import (
    BackupExportSpec,
    RestoreFromBackupSpec,
    SnapshotSpec,
)
from Agent.models.scenarios.runs import ScenarioRun
from Agent.utility.rest_client import IncusRestClient
from Utilities import consts
from Utilities.logger import Logger, LoggLevel


logger = Logger("[SCENARIO.DATA]", consts.ConfigVariables.DEFAULT_LOGS_INCUS.value)


class InstanceDataScenarios:
    def __init__(self, client: IncusRestClient):
        self._client = client
        self._instances = InstancesController(client)
        self._snapshots = InstancesSnapshotsController(client)
        self._backups = InstancesBackupsController(client)

    # Scenario: instance.snapshot
    async def snapshot(self, spec: SnapshotSpec) -> ScenarioRun:
        snap_name = spec.name or _timestamp_name("snap")
        logger.line(f"Invoke snapshot instance={spec.instance} snapshot={snap_name} stateful={spec.stateful} keep_last_n={spec.keep_last_n}", LoggLevel.INFO)
        runner = ScenarioRunner("instance.snapshot", target=spec.instance)

        async with runner.step("create_snapshot") as step:
            body: dict[str, Any] = {"name": snap_name, "stateful": spec.stateful}
            if spec.expires_at:
                body["expires_at"] = spec.expires_at
            await self._snapshots.create_snapshot(spec.instance, body=body, project=spec.project)
            step.detail["snapshot"] = snap_name
            step.detail["stateful"] = spec.stateful

        if spec.keep_last_n is not None and spec.keep_last_n > 0:
            async with runner.step("prune") as step:
                deleted = await _helpers.prune_old_snapshots(
                    self._client,
                    instance=spec.instance,
                    keep_last_n=spec.keep_last_n,
                    project=spec.project,
                )
                step.detail["deleted"] = deleted
                step.detail["kept"] = spec.keep_last_n
        else:
            runner.skip("prune", reason="spec.keep_last_n not set")

        return runner.finish(result={"instance": spec.instance, "snapshot": snap_name})

    # Scenario: instance.backup_export
    #
    # Creates a backup. The actual binary export must be fetched via the raw
    # endpoint GET /instances/{name}/backups/{backup}/export. This scenario
    # returns the resulting URL so the client can stream it down.
    async def backup_export(self, spec: BackupExportSpec) -> ScenarioRun:
        backup_name = spec.name or _timestamp_name("backup")
        logger.line(f"Invoke backup_export instance={spec.instance} backup={backup_name} compression={spec.compression_algorithm} optimized={spec.optimized_storage}", LoggLevel.INFO)
        runner = ScenarioRunner("instance.backup_export", target=spec.instance)

        async with runner.step("create_backup") as step:
            body: dict[str, Any] = {
                "name": backup_name,
                "instance_only": spec.instance_only,
                "optimized_storage": spec.optimized_storage,
            }
            if spec.compression_algorithm:
                body["compression_algorithm"] = spec.compression_algorithm
            await self._backups.create_backup(spec.instance, body=body, project=spec.project)
            step.detail["backup"] = backup_name

        export_url = (
            f"/instances/{spec.instance}/backups/{backup_name}/export"
            f"?project={spec.project}"
        )
        return runner.finish(result={
            "instance": spec.instance,
            "backup": backup_name,
            "export_url": export_url,
        })

    # Scenario: instance.restore_from_backup
    #
    # Thin orchestration shell. The backup *bytes* must already be uploaded
    # to the agent through the raw image-import endpoint
    # (POST /instances with Content-Type: application/octet-stream and
    # X-Incus-name header). This scenario covers the post-upload flow:
    # optionally rename, optionally start.
    async def restore_from_backup(self, spec: RestoreFromBackupSpec) -> ScenarioRun:
        logger.line(f"Invoke restore_from_backup backup={spec.backup_name} target={spec.target_name} project={spec.project} start_after={spec.start_after}", LoggLevel.INFO)
        runner = ScenarioRunner("instance.restore_from_backup", target=spec.target_name or spec.backup_name)

        async with runner.step("verify_imported") as step:
            imported_name = spec.target_name or spec.backup_name
            await self._instances.instance_info(name=imported_name, project=spec.project)
            step.detail["imported_as"] = imported_name

        if spec.target_name and spec.target_name != spec.backup_name:
            async with runner.step("rename") as step:
                await self._instances.rename_instance(
                    name=spec.backup_name,
                    new_name=spec.target_name,
                    project=spec.project,
                )
                step.detail["renamed_to"] = spec.target_name
        else:
            runner.skip("rename", reason="target_name same as backup_name")

        if spec.start_after:
            async with runner.step("start") as step:
                await self._instances.set_instance_state(
                    spec.target_name or spec.backup_name,
                    action="start",
                    project=spec.project,
                )
                step.detail["started"] = True
        else:
            runner.skip("start", reason="spec.start_after=false")

        return runner.finish(result={"name": spec.target_name or spec.backup_name})


def _timestamp_name(prefix: str) -> str:
    return f"{prefix}-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
