"""Boilerplate rawCommand controller. Real commands (apt update,
systemctl restart incus, journalctl tail, etc.) follow this pattern:
declare argv, delegate to _executor.run, return CommandResult.
"""
from Agent.controllers.agent.rawCommands._executor import CommandResult, run
from Utilities import consts
from Utilities.logger import Logger, LoggLevel


logger = Logger("[RAW.EXAMPLES]", consts.ConfigVariables.DEFAULT_LOGS_INCUS.value)


class RawCommandsController:

    #Command to check incus status
    async def HealthCheckIncus(self) -> CommandResult:
        logger.line("Checking incus health", LoggLevel.INFO)
        return await run(["systemctl", "status", "incus.service"], timeout=5.0)
