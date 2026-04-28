"""Boilerplate rawCommand controller. Real commands (apt update,
systemctl restart incus, journalctl tail, etc.) follow this pattern:
declare argv, delegate to _executor.run, return CommandResult.
"""
from Agent.controllers.agent.rawCommands._executor import CommandResult, run
from Utilities import consts
from Utilities.logger import Logger, LoggLevel


logger = Logger("[RAW.EXAMPLES]", consts.ConfigVariables.DEFAULT_LOGS_INCUS.value)


class ExamplesController:
    # rawCommand: examples.echo_dupa
    async def echo_dupa(self) -> CommandResult:
        logger.line("Invoke echo_dupa", LoggLevel.INFO)
        return await run(["echo", "dupa"], timeout=5.0)
