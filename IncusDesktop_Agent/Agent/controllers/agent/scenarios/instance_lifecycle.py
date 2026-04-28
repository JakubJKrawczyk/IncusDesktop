from datetime import datetime, timezone
from typing import Any

from Agent.controllers.agent.scenarios import _helpers
from Agent.controllers.agent.scenarios._runner import ScenarioRunner
from Agent.controllers.incus.instances import InstancesController
from Agent.controllers.incus.instances_snapshots import InstancesSnapshotsController
from Agent.models.scenarios.instance import (
    CloneSpec,
    DecommissionSpec,
    ProvisionSpec,
    ResetToSnapshotSpec,
    RestartSpec,
)
from Agent.models.scenarios.runs import ScenarioRun
from Agent.utility.rest_client import IncusError, IncusRestClient
from Utilities import consts
from Utilities.logger import Logger, LoggLevel


logger = Logger("[SCENARIO.LIFECYCLE]", consts.ConfigVariables.DEFAULT_LOGS_INCUS.value)


class InstanceLifecycleScenarios:
    def __init__(self, client: IncusRestClient):
        self._client = client
        self._instances = InstancesController(client)
        self._snapshots = InstancesSnapshotsController(client)

    # Scenario: instance.provision
    async def provision(self, spec: ProvisionSpec) -> ScenarioRun:
        logger.line(f"Invoke provision name={spec.name} image={spec.image_alias} project={spec.project} cpu={spec.cpu} memory={spec.memory}", LoggLevel.INFO)
        runner = ScenarioRunner("instance.provision", target=spec.name)

        async with runner.step("ensure_image") as step:
            fingerprint = await _helpers.ensure_image(
                self._client,
                spec.image_alias,
                server=spec.image_server,
                protocol=spec.image_protocol,
                project=spec.project,
            )
            step.detail["fingerprint"] = fingerprint

        async with runner.step("create_instance") as step:
            config, devices = self._build_config_devices(spec)
            body: dict[str, Any] = {
                "name": spec.name,
                "type": spec.instance_type,
                "source": {"type": "image", "fingerprint": fingerprint},
                "profiles": spec.profiles,
                "config": config,
                "devices": devices,
            }
            await self._instances.create_instance(body=body, project=spec.project)
            step.detail["config_keys"] = list(config.keys())
            step.detail["device_keys"] = list(devices.keys())

        if not spec.start:
            runner.skip("start", reason="spec.start=false")
            runner.skip("wait_agent", reason="spec.start=false")
            return runner.finish(result={"name": spec.name, "fingerprint": fingerprint, "started": False})

        async with runner.step("start") as step:
            await self._instances.set_instance_state(spec.name, action="start", project=spec.project)
            step.detail["action"] = "start"

        if spec.wait_agent:
            async with runner.step("wait_agent") as step:
                ready = await _helpers.wait_agent_ready(
                    self._client,
                    spec.name,
                    project=spec.project,
                    timeout=spec.wait_agent_timeout,
                )
                step.detail["ready"] = ready
                step.detail["timeout_seconds"] = spec.wait_agent_timeout
                if not ready:
                    raise IncusError(f"agent not ready within {spec.wait_agent_timeout}s")
        else:
            runner.skip("wait_agent", reason="spec.wait_agent=false")

        return runner.finish(result={"name": spec.name, "fingerprint": fingerprint, "started": True})

    @staticmethod
    def _build_config_devices(spec: ProvisionSpec) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
        config: dict[str, Any] = dict(spec.extra_config)
        if spec.cpu is not None:
            config.setdefault("limits.cpu", str(spec.cpu))
        if spec.memory is not None:
            config.setdefault("limits.memory", spec.memory)
        if spec.ssh_pubkey or spec.cloud_init_user_data:
            config.setdefault(
                "user.user-data",
                _helpers.build_cloud_init_user_data(
                    ssh_pubkey=spec.ssh_pubkey,
                    extra_user_data=spec.cloud_init_user_data,
                ),
            )

        devices: dict[str, dict[str, Any]] = {
            k: dict(v) for k, v in spec.extra_devices.items()
        }
        if spec.network:
            devices.setdefault("eth0", {
                "type": "nic",
                "nictype": "bridged",
                "parent": spec.network,
            })
        if spec.root_disk_size:
            devices.setdefault("root", {
                "type": "disk",
                "path": "/",
                "pool": "default",
                "size": spec.root_disk_size,
            })
        return config, devices

    # Scenario: instance.clone
    async def clone(self, spec: CloneSpec) -> ScenarioRun:
        logger.line(f"Invoke clone source={spec.source_name} target={spec.target_name} project={spec.project}", LoggLevel.INFO)
        runner = ScenarioRunner("instance.clone", target=spec.target_name)

        async with runner.step("verify_source") as step:
            await self._instances.instance_info(name=spec.source_name, project=spec.project)
            step.detail["source"] = spec.source_name

        async with runner.step("copy_instance") as step:
            source: dict[str, Any] = {
                "type": "copy",
                "source": spec.source_name,
                "instance_only": spec.instance_only,
            }
            if spec.snapshot:
                source["source_snapshot"] = spec.snapshot
            if spec.target_project and spec.target_project != spec.project:
                source["project"] = spec.project

            body: dict[str, Any] = {"name": spec.target_name, "source": source}
            target_project = spec.target_project or spec.project
            await self._instances.create_instance(body=body, project=target_project)
            step.detail["target"] = spec.target_name
            step.detail["target_project"] = target_project

        if spec.start:
            async with runner.step("start") as step:
                await self._instances.set_instance_state(
                    spec.target_name,
                    action="start",
                    project=spec.target_project or spec.project,
                )
                step.detail["action"] = "start"
        else:
            runner.skip("start", reason="spec.start=false")

        return runner.finish(result={
            "source": spec.source_name,
            "target": spec.target_name,
            "started": spec.start,
        })

    # Scenario: instance.decommission
    async def decommission(self, spec: DecommissionSpec) -> ScenarioRun:
        logger.line(f"Invoke decommission name={spec.name} project={spec.project} final_snapshot={spec.final_snapshot}", LoggLevel.INFO)
        runner = ScenarioRunner("instance.decommission", target=spec.name)

        async with runner.step("stop") as step:
            try:
                await self._instances.set_instance_state(
                    spec.name,
                    action="stop",
                    timeout=spec.stop_timeout,
                    force=spec.force_stop,
                    project=spec.project,
                )
                step.detail["action"] = "stop"
            except IncusError as exc:
                step.detail["note"] = f"stop attempt: {exc}"

        if spec.final_snapshot:
            snap_name = spec.final_snapshot_name or _timestamp_name("pre-delete")
            async with runner.step("final_snapshot") as step:
                await self._snapshots.create_snapshot(
                    spec.name,
                    body={"name": snap_name, "stateful": False},
                    project=spec.project,
                )
                step.detail["snapshot"] = snap_name
        else:
            runner.skip("final_snapshot", reason="spec.final_snapshot=false")

        async with runner.step("delete") as step:
            await self._instances.delete_instance(name=spec.name, project=spec.project)
            step.detail["deleted"] = spec.name

        return runner.finish(result={"name": spec.name, "deleted": True})

    # Scenario: instance.reset_to_snapshot
    async def reset_to_snapshot(self, spec: ResetToSnapshotSpec) -> ScenarioRun:
        logger.line(f"Invoke reset_to_snapshot name={spec.name} snapshot={spec.snapshot} project={spec.project}", LoggLevel.INFO)
        runner = ScenarioRunner("instance.reset_to_snapshot", target=spec.name)

        async with runner.step("stop") as step:
            try:
                await self._instances.set_instance_state(
                    spec.name, action="stop", force=True, project=spec.project,
                )
                step.detail["action"] = "stop"
            except IncusError as exc:
                step.detail["note"] = f"stop: {exc}"

        async with runner.step("restore") as step:
            await self._instances.update_instance(
                name=spec.name,
                body={"restore": spec.snapshot},
                project=spec.project,
            )
            step.detail["snapshot"] = spec.snapshot

        if spec.start_after:
            async with runner.step("start") as step:
                await self._instances.set_instance_state(
                    spec.name, action="start", project=spec.project,
                )
                step.detail["action"] = "start"
        else:
            runner.skip("start", reason="spec.start_after=false")

        return runner.finish(result={"name": spec.name, "restored_from": spec.snapshot})

    # Scenario: instance.restart
    async def restart(self, spec: RestartSpec) -> ScenarioRun:
        logger.line(f"Invoke restart name={spec.name} project={spec.project} timeout={spec.timeout} force={spec.force}", LoggLevel.INFO)
        runner = ScenarioRunner("instance.restart", target=spec.name)

        async with runner.step("restart") as step:
            await self._instances.set_instance_state(
                spec.name,
                action="restart",
                timeout=spec.timeout,
                force=spec.force,
                project=spec.project,
            )
            step.detail["timeout"] = spec.timeout
            step.detail["force"] = spec.force

        return runner.finish(result={"name": spec.name})


def _timestamp_name(prefix: str) -> str:
    return f"{prefix}-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
