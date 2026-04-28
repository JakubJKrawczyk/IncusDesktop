from typing import Any

from Agent.controllers.agent.scenarios import _helpers
from Agent.controllers.agent.scenarios._runner import ScenarioRunner
from Agent.controllers.incus.profiles import ProfilesController
from Agent.controllers.incus.projects import ProjectsController
from Agent.models.scenarios.host import HostBootstrapSpec, ProjectBootstrapSpec
from Agent.models.scenarios.runs import ScenarioRun
from Agent.utility.rest_client import IncusError, IncusRestClient
from Utilities import consts
from Utilities.logger import Logger, LoggLevel


logger = Logger("[SCENARIO.HOST]", consts.ConfigVariables.DEFAULT_LOGS_INCUS.value)


class HostSetupScenarios:
    def __init__(self, client: IncusRestClient):
        self._client = client
        self._profiles = ProfilesController(client)
        self._projects = ProjectsController(client)

    # Scenario: host.bootstrap
    async def host_bootstrap(self, spec: HostBootstrapSpec) -> ScenarioRun:
        logger.line(f"Invoke host_bootstrap pool={spec.storage_pool_name} driver={spec.storage_pool_driver} network={spec.network_name} type={spec.network_type}", LoggLevel.INFO)
        runner = ScenarioRunner("host.bootstrap")

        async with runner.step("ensure_storage_pool") as step:
            created = await _helpers.ensure_storage_pool(
                self._client,
                name=spec.storage_pool_name,
                driver=spec.storage_pool_driver,
                config=spec.storage_pool_config,
            )
            step.detail["pool"] = spec.storage_pool_name
            step.detail["created"] = created

        async with runner.step("ensure_network") as step:
            created = await _helpers.ensure_network(
                self._client,
                name=spec.network_name,
                type=spec.network_type,
                config=spec.network_config,
            )
            step.detail["network"] = spec.network_name
            step.detail["created"] = created

        if spec.attach_to_default_profile:
            async with runner.step("attach_default_profile_devices") as step:
                devices_patch: dict[str, dict[str, Any]] = {
                    "root": {
                        "type": "disk",
                        "path": "/",
                        "pool": spec.storage_pool_name,
                    },
                    "eth0": {
                        "type": "nic",
                        "network": spec.network_name,
                    },
                }
                await self._profiles.patch_profile(
                    name="default",
                    body={"devices": devices_patch},
                    project="default",
                )
                step.detail["devices"] = list(devices_patch.keys())
        else:
            runner.skip("attach_default_profile_devices", reason="spec.attach_to_default_profile=false")

        return runner.finish(result={
            "pool": spec.storage_pool_name,
            "network": spec.network_name,
        })

    # Scenario: project.bootstrap
    async def project_bootstrap(self, spec: ProjectBootstrapSpec) -> ScenarioRun:
        logger.line(f"Invoke project_bootstrap name={spec.name} create_default_profile={spec.create_default_profile}", LoggLevel.INFO)
        runner = ScenarioRunner("project.bootstrap", target=spec.name)

        async with runner.step("create_project") as step:
            try:
                await self._projects.project_info(spec.name)
                step.detail["existed"] = True
            except IncusError:
                body: dict[str, Any] = {"name": spec.name, "config": spec.config}
                if spec.description:
                    body["description"] = spec.description
                await self._projects.create_project(body=body)
                step.detail["existed"] = False
            step.detail["project"] = spec.name

        if spec.create_default_profile:
            async with runner.step("ensure_default_profile") as step:
                created = await _helpers.ensure_profile(
                    self._client,
                    name="default",
                    config=spec.profile_config,
                    devices=spec.profile_devices,
                    project=spec.name,
                )
                step.detail["created"] = created
        else:
            runner.skip("ensure_default_profile", reason="spec.create_default_profile=false")

        return runner.finish(result={"project": spec.name})
