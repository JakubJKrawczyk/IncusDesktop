import asyncio
from typing import Any

from Agent.controllers.agent.scenarios._runner import ScenarioRunner
from Agent.controllers.incus.instances import InstancesController
from Agent.controllers.incus.instances_backups import InstancesBackupsController
from Agent.controllers.incus.instances_snapshots import InstancesSnapshotsController
from Agent.controllers.incus.networks import NetworksController
from Agent.controllers.incus.server import ServerController
from Agent.controllers.incus.storage_pools import StoragePoolsController
from Agent.models.scenarios.runs import ScenarioRun
from Agent.utility.rest_client import IncusError, IncusRestClient
from Utilities import consts
from Utilities.logger import Logger, LoggLevel


logger = Logger("[SCENARIO.DASHBOARD]", consts.ConfigVariables.DEFAULT_LOGS_INCUS.value)


class DashboardScenarios:
    def __init__(self, client: IncusRestClient):
        self._client = client
        self._server = ServerController(client)
        self._instances = InstancesController(client)
        self._snapshots = InstancesSnapshotsController(client)
        self._backups = InstancesBackupsController(client)
        self._networks = NetworksController(client)
        self._pools = StoragePoolsController(client)

    # Scenario: dashboard
    #
    # Aggregates a snapshot of host state in one response. Calls run in
    # parallel with asyncio.gather. Per-section errors are isolated — a
    # failure on /networks doesn't block /instances.
    async def dashboard(self, project: str = "default") -> ScenarioRun:
        logger.line(f"Invoke dashboard project={project}", LoggLevel.INFO)
        runner = ScenarioRunner("dashboard")

        async with runner.step("gather") as step:
            results = await asyncio.gather(
                _safe(self._server.server_info()),
                _safe(self._server.resources()),
                _safe(self._instances.list_instances(project=project)),
                _safe(self._networks.list_networks(recursion=1, project=project)),
                _safe(self._pools.list_pools(recursion=1)),
                return_exceptions=False,
            )
            server_info, resources, instances, networks, pools = results
            step.detail["sections"] = ["server", "resources", "instances", "networks", "pools"]

        return runner.finish(result={
            "project": project,
            "server": server_info,
            "resources": resources,
            "instances": instances,
            "networks": networks,
            "storage_pools": pools,
        })

    # Scenario: instance.full
    async def instance_full(self, name: str, project: str = "default") -> ScenarioRun:
        logger.line(f"Invoke instance_full name={name} project={project}", LoggLevel.INFO)
        runner = ScenarioRunner("instance.full", target=name)

        async with runner.step("gather") as step:
            results = await asyncio.gather(
                _safe(self._instances.instance_info(name=name, project=project)),
                _safe(self._instances.instance_state(name=name, project=project)),
                _safe(self._snapshots.list_snapshots(name=name, recursion=1, project=project)),
                _safe(self._backups.list_backups(name=name, recursion=1, project=project)),
                return_exceptions=False,
            )
            info, state, snapshots, backups = results
            step.detail["sections"] = ["info", "state", "snapshots", "backups"]

        return runner.finish(result={
            "name": name,
            "info": info,
            "state": state,
            "snapshots": snapshots,
            "backups": backups,
        })


async def _safe(coro) -> Any:
    """Await coro and return its result, or {"error": str(exc)} on failure."""
    try:
        return await coro
    except IncusError as exc:
        return {"error": str(exc)}
    except Exception as exc:
        return {"error": f"{type(exc).__name__}: {exc}"}
