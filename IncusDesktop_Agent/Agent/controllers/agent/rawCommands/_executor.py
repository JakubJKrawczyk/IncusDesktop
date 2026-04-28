"""Async subprocess wrapper for rawCommands.

Each rawCommand controller dispatches to `run` with a fixed argv vector.
We never accept user-supplied shell strings here — argv only — to keep
this layer auditable. Future commands like `apt update`, `systemctl
restart incus` should be added as discrete typed methods, not generic
shell-out endpoints.
"""
import asyncio
from dataclasses import dataclass

from Utilities import consts
from Utilities.logger import Logger, LoggLevel


logger = Logger("[RAW.EXEC]", consts.ConfigVariables.DEFAULT_LOGS_INCUS.value)


@dataclass
class CommandResult:
    command: list[str]
    return_code: int
    stdout: str
    stderr: str
    timed_out: bool


async def run(
    argv: list[str],
    *,
    timeout: float = 30.0,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
) -> CommandResult:
    """Execute argv with a timeout. Returns a CommandResult; never raises
    on non-zero exit. Raises only on spawn failure."""
    if not argv:
        raise ValueError("argv must be a non-empty list")

    logger.line(f"Spawning argv={argv} timeout={timeout}s cwd={cwd}", LoggLevel.INFO)
    proc = await asyncio.create_subprocess_exec(
        *argv,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=cwd,
        env=env,
    )
    try:
        stdout_b, stderr_b = await asyncio.wait_for(proc.communicate(), timeout=timeout)
        timed_out = False
    except asyncio.TimeoutError:
        proc.kill()
        stdout_b, stderr_b = await proc.communicate()
        timed_out = True
        logger.line(f"Command timed out argv={argv} timeout={timeout}s", LoggLevel.WARNING)

    return_code = proc.returncode if proc.returncode is not None else -1
    level = LoggLevel.INFO if return_code == 0 and not timed_out else LoggLevel.ERROR
    logger.line(f"Command finished argv={argv} return_code={return_code} timed_out={timed_out}", level)

    return CommandResult(
        command=list(argv),
        return_code=return_code,
        stdout=stdout_b.decode("utf-8", errors="replace"),
        stderr=stderr_b.decode("utf-8", errors="replace"),
        timed_out=timed_out,
    )
