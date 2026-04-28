from typing import Any

from Agent.controllers.agent.scenarios import _helpers
from Agent.controllers.agent.scenarios._runner import ScenarioRunner
from Agent.controllers.incus.instances import InstancesController
from Agent.controllers.incus.instances_exec import InstancesExecController
from Agent.models.scenarios.instance import (
    AttachNetworkSpec,
    AttachVolumeSpec,
    ExposePortSpec,
    ResourceUpdateSpec,
    RunCommandSpec,
)
from Agent.models.scenarios.runs import ScenarioRun
from Agent.utility.rest_client import IncusError, IncusRestClient
from Utilities import consts
from Utilities.logger import Logger, LoggLevel


logger = Logger("[SCENARIO.CONFIG]", consts.ConfigVariables.DEFAULT_LOGS_INCUS.value)


class InstanceConfigScenarios:
    def __init__(self, client: IncusRestClient):
        self._client = client
        self._instances = InstancesController(client)
        self._exec = InstancesExecController(client)

    # Scenario: instance.update_resources
    async def update_resources(self, spec: ResourceUpdateSpec) -> ScenarioRun:
        logger.line(f"Invoke update_resources name={spec.name} cpu={spec.cpu} memory={spec.memory} root_disk={spec.root_disk_size}", LoggLevel.INFO)
        runner = ScenarioRunner("instance.update_resources", target=spec.name)

        async with runner.step("read_state") as step:
            info = await self._instances.instance_info(spec.name, project=spec.project)
            running = _is_running(info)
            step.detail["running"] = running

        async with runner.step("patch_config") as step:
            patch_body = {"config": {}, "devices": {}}
            if spec.cpu is not None:
                patch_body["config"]["limits.cpu"] = str(spec.cpu)
            if spec.memory is not None:
                patch_body["config"]["limits.memory"] = spec.memory
            if spec.root_disk_size is not None:
                patch_body["devices"]["root"] = {
                    "type": "disk",
                    "path": "/",
                    "pool": "default",
                    "size": spec.root_disk_size,
                }
            if not patch_body["config"] and not patch_body["devices"]:
                step.detail["note"] = "nothing to change"
                runner.skip("restart", reason="no changes")
                return runner.finish(result={"name": spec.name, "changed": False})

            await self._instances.patch_instance(spec.name, body=patch_body, project=spec.project)
            step.detail["applied"] = patch_body

        if spec.restart_if_required and running:
            async with runner.step("restart") as step:
                await self._instances.set_instance_state(
                    spec.name, action="restart", project=spec.project,
                )
                step.detail["restarted"] = True
        else:
            runner.skip("restart", reason="not running or restart disabled")

        return runner.finish(result={"name": spec.name, "changed": True})

    # Scenario: instance.attach_volume
    async def attach_volume(self, spec: AttachVolumeSpec) -> ScenarioRun:
        logger.line(f"Invoke attach_volume instance={spec.instance} pool={spec.pool} volume={spec.volume} create_if_missing={spec.create_if_missing}", LoggLevel.INFO)
        runner = ScenarioRunner("instance.attach_volume", target=spec.instance)

        if spec.create_if_missing:
            async with runner.step("ensure_volume") as step:
                created = await _helpers.ensure_storage_volume(
                    self._client,
                    pool=spec.pool,
                    name=spec.volume,
                    type="custom",
                    size=spec.volume_size,
                    project=spec.project,
                )
                step.detail["volume"] = spec.volume
                step.detail["created"] = created
        else:
            runner.skip("ensure_volume", reason="spec.create_if_missing=false")

        async with runner.step("attach_device") as step:
            device_name = spec.device_name or spec.volume
            device: dict[str, Any] = {
                "type": "disk",
                "pool": spec.pool,
                "source": spec.volume,
            }
            if spec.mount_path:
                device["path"] = spec.mount_path
            if spec.readonly:
                device["readonly"] = "true"

            await self._instances.patch_instance(
                spec.instance,
                body={"devices": {device_name: device}},
                project=spec.project,
            )
            step.detail["device_name"] = device_name

        if spec.restart_instance:
            async with runner.step("restart") as step:
                await self._instances.set_instance_state(
                    spec.instance, action="restart", project=spec.project,
                )
                step.detail["restarted"] = True
        else:
            runner.skip("restart", reason="spec.restart_instance=false")

        return runner.finish(result={
            "instance": spec.instance,
            "device": spec.device_name or spec.volume,
        })

    # Scenario: instance.attach_network
    async def attach_network(self, spec: AttachNetworkSpec) -> ScenarioRun:
        logger.line(f"Invoke attach_network instance={spec.instance} network={spec.network} nic_type={spec.nic_type}", LoggLevel.INFO)
        runner = ScenarioRunner("instance.attach_network", target=spec.instance)

        async with runner.step("read_state") as step:
            info = await self._instances.instance_info(spec.instance, project=spec.project)
            existing_devices = _get_devices(info)
            device_name = spec.device_name or _next_eth_name(existing_devices)
            step.detail["device_name"] = device_name
            step.detail["running"] = _is_running(info)

        async with runner.step("attach_device") as step:
            device: dict[str, Any] = {
                "type": "nic",
                "nictype": spec.nic_type,
                "parent": spec.network,
            }
            if spec.ipv4_address:
                device["ipv4.address"] = spec.ipv4_address
            if spec.ipv6_address:
                device["ipv6.address"] = spec.ipv6_address

            await self._instances.patch_instance(
                spec.instance,
                body={"devices": {device_name: device}},
                project=spec.project,
            )
            step.detail["device_name"] = device_name
            step.detail["network"] = spec.network

        if spec.restart_instance:
            async with runner.step("restart") as step:
                await self._instances.set_instance_state(
                    spec.instance, action="restart", project=spec.project,
                )
                step.detail["restarted"] = True
        else:
            runner.skip("restart", reason="spec.restart_instance=false")

        return runner.finish(result={
            "instance": spec.instance,
            "device": device_name,
            "network": spec.network,
        })

    # Scenario: instance.expose_port
    async def expose_port(self, spec: ExposePortSpec) -> ScenarioRun:
        logger.line(f"Invoke expose_port instance={spec.instance} network={spec.network} listen={spec.listen_address} target_port={spec.target_port}", LoggLevel.INFO)
        runner = ScenarioRunner("instance.expose_port", target=spec.instance)

        async with runner.step("resolve_target_address") as step:
            state = await self._instances.instance_state(spec.instance, project=spec.project)
            target_address = _first_global_ipv4(state)
            if not target_address:
                raise IncusError(f"instance {spec.instance!r} has no reachable IPv4")
            step.detail["target_address"] = target_address

        listen_port = spec.listen_port or spec.target_port
        port_entry: dict[str, Any] = {
            "protocol": spec.protocol,
            "listen_port": str(listen_port),
            "target_port": str(spec.target_port),
            "target_address": target_address,
        }
        if spec.description:
            port_entry["description"] = spec.description

        async with runner.step("ensure_forward") as step:
            created = await _helpers.ensure_network_forward(
                self._client,
                network=spec.network,
                listen_address=spec.listen_address,
                ports=[port_entry],
                project=spec.project,
            )
            step.detail["created_forward"] = created
            if not created:
                step.detail["note"] = "forward already exists; appending port via patch"
                await self._patch_forward_append_port(
                    spec.network, spec.listen_address, port_entry, project=spec.project,
                )

        return runner.finish(result={
            "instance": spec.instance,
            "listen": f"{spec.listen_address}:{listen_port}",
            "target": f"{target_address}:{spec.target_port}",
        })

    async def _patch_forward_append_port(
        self,
        network: str,
        listen_address: str,
        port_entry: dict[str, Any],
        project: str,
    ) -> None:
        from Agent.controllers.incus.networks_forwards import NetworksForwardsController
        forwards = NetworksForwardsController(self._client)
        existing = await forwards.forward_info(network, listen_address, project=project)
        ports = existing.get("ports") if isinstance(existing, dict) else (getattr(existing, "ports", None) or [])
        new_ports = list(ports or []) + [port_entry]
        await forwards.patch_forward(
            network, listen_address,
            body={"ports": new_ports},
            project=project,
        )

    # Scenario: instance.run_command
    async def run_command(self, spec: RunCommandSpec) -> ScenarioRun:
        logger.line(f"Invoke run_command instance={spec.instance} command={spec.command} timeout={spec.timeout_seconds}", LoggLevel.INFO)
        runner = ScenarioRunner("instance.run_command", target=spec.instance)

        async with runner.step("exec") as step:
            body: dict[str, Any] = {
                "command": spec.command,
                "user": spec.user,
                "group": spec.group,
                "environment": spec.environment,
                "wait-for-websocket": False,
                "record-output": spec.capture_output,
                "interactive": False,
            }
            if spec.cwd:
                body["cwd"] = spec.cwd

            metadata = await self._client.post(
                f"/1.0/instances/{spec.instance}/exec",
                json_body=body,
                params={"project": spec.project},
                wait=True,
                wait_timeout=spec.timeout_seconds,
            )
            inner = metadata.get("metadata") if isinstance(metadata, dict) else {}
            return_code = (inner or {}).get("return") if isinstance(inner, dict) else None
            output = (inner or {}).get("output") if isinstance(inner, dict) else None
            step.detail["return_code"] = return_code
            step.detail["output_paths"] = output

        stdout = stderr = ""
        if spec.capture_output and isinstance(step.detail.get("output_paths"), dict):
            async with runner.step("collect_output") as step2:
                stdout = await _read_output(
                    self._exec, spec.instance,
                    step.detail["output_paths"].get("1"),
                    project=spec.project,
                )
                stderr = await _read_output(
                    self._exec, spec.instance,
                    step.detail["output_paths"].get("2"),
                    project=spec.project,
                )
                step2.detail["stdout_bytes"] = len(stdout)
                step2.detail["stderr_bytes"] = len(stderr)
        else:
            runner.skip("collect_output", reason="capture_output=false or no output paths")

        return runner.finish(result={
            "instance": spec.instance,
            "return_code": step.detail.get("return_code"),
            "stdout": stdout,
            "stderr": stderr,
        })


# ─── module helpers ────────────────────────────────────────────────────────

def _is_running(info: Any) -> bool:
    status = info.get("status") if isinstance(info, dict) else getattr(info, "status", None)
    return str(status or "").lower() == "running"


def _get_devices(info: Any) -> dict[str, dict[str, Any]]:
    devices = info.get("devices") if isinstance(info, dict) else getattr(info, "devices", None)
    return devices if isinstance(devices, dict) else {}


def _next_eth_name(devices: dict[str, dict[str, Any]]) -> str:
    used = {n for n in devices.keys() if n.startswith("eth") and n[3:].isdigit()}
    i = 0
    while f"eth{i}" in used:
        i += 1
    return f"eth{i}"


def _first_global_ipv4(state: Any) -> str | None:
    network = state.get("network") if isinstance(state, dict) else getattr(state, "network", None)
    if not isinstance(network, dict):
        return None
    for iface_name, iface in network.items():
        if iface_name == "lo" or not isinstance(iface, dict):
            continue
        for addr in iface.get("addresses", []) or []:
            if not isinstance(addr, dict):
                continue
            if addr.get("family") == "inet" and addr.get("scope") == "global":
                return addr.get("address")
    return None


async def _read_output(exec_ctrl: InstancesExecController, instance: str, path: str | None, project: str) -> str:
    if not path:
        return ""
    filename = path.rsplit("/", 1)[-1]
    try:
        data = await exec_ctrl.get_exec_output(instance, filename, project=project)
        return data.decode("utf-8", errors="replace") if isinstance(data, (bytes, bytearray)) else str(data)
    except IncusError:
        return ""
