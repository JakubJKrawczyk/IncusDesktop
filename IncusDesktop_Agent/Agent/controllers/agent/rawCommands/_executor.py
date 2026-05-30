"""Async subprocess wrapper for rawCommands.

Each rawCommand controller dispatches to `run` with a fixed argv vector.
We never accept user-supplied shell strings here — argv only — to keep
this layer auditable. Future commands like `apt update`, `systemctl
restart incus` should be added as discrete typed methods, not generic
shell-out endpoints.

Error model — strict by default:
  - Empty argv: raises ValueError (programmer error, not user-facing).
  - Spawn failures (missing binary, permission denied):
    raise CommandFailedError.
  - Timeout: raises CommandTimeoutError.
  - Non-zero exit: raises CommandFailedError.
  - Success (return_code == 0) is the only path that returns a
    CommandResult.

If a caller has a legitimate reason to accept a non-zero exit
(e.g. `systemctl is-active` returns 3 for inactive units), it must
wrap the call in try/except CommandFailedError and inspect
exc.details["return_code"].
"""
import asyncio
from dataclasses import dataclass

from Agent.exceptions import CommandFailedError, CommandTimeoutError
from Utilities import consts
from Utilities.logger import Logger, LoggLevel


logger = Logger("[RAW.EXEC]", consts.ConfigVariables.DEFAULT_LOGS_INCUS.value)


@dataclass
class CommandResult:
    command: list[str]
    return_code: int
    stdout: str
    stderr: str


async def run(
    argv: list[str],
    *,
    timeout: float = 30.0,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
) -> CommandResult:
    """Execute argv with a timeout.

    Returns CommandResult on success (return_code == 0). Raises
    CommandTimeoutError on timeout, CommandFailedError on non-zero
    exit or spawn failure.
    """
    if not argv:
        raise ValueError("argv must be a non-empty list")

    logger.line(f"Spawning argv={argv} timeout={timeout}s cwd={cwd}", LoggLevel.INFO)
    try:
        proc = await asyncio.create_subprocess_exec(
            *argv,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd,
            env=env,
        )
    except FileNotFoundError as exc:
        logger.line(f"Binary not found: {argv[0]!r}", LoggLevel.ERROR)
        raise CommandFailedError(
            f"Required binary not found: {argv[0]!r}.",
            details={"argv": list(argv), "missing_binary": argv[0]},
            user_action=f"Install {argv[0]!r} on the host or remove the feature that depends on it.",
        ) from exc
    except PermissionError as exc:
        logger.line(f"Permission denied launching: {argv[0]!r}", LoggLevel.ERROR)
        raise CommandFailedError(
            f"Permission denied launching {argv[0]!r}.",
            details={"argv": list(argv)},
        ) from exc

    try:
        stdout_b, stderr_b = await asyncio.wait_for(proc.communicate(), timeout=timeout)
        timed_out = False
    except asyncio.TimeoutError:
        proc.kill()
        stdout_b, stderr_b = await proc.communicate()
        timed_out = True
        logger.line(f"Command timed out argv={argv} timeout={timeout}s", LoggLevel.WARNING)

    return_code = proc.returncode if proc.returncode is not None else -1
    stdout = stdout_b.decode("utf-8", errors="replace")
    stderr = stderr_b.decode("utf-8", errors="replace")

    if timed_out:
        raise CommandTimeoutError(
            f"Command timed out after {timeout}s.",
            details={
                "argv": list(argv),
                "timeout": timeout,
                "stderr_excerpt": stderr[:500],
            },
        )

    if return_code != 0:
        logger.line(f"Command finished argv={argv} return_code={return_code}", LoggLevel.ERROR)
        raise CommandFailedError(
            f"Command exited with code {return_code}.",
            details={
                "argv": list(argv),
                "return_code": return_code,
                "stderr_excerpt": stderr[:500],
            },
        )

    logger.line(f"Command finished argv={argv} return_code={return_code}", LoggLevel.INFO)
    return CommandResult(
        command=list(argv),
        return_code=return_code,
        stdout=stdout,
        stderr=stderr,
    )
