import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Any

from Agent.controllers.agent.scenarios import _store
from Agent.models.scenarios.runs import ScenarioRun, StepResult, StepStatus
from Utilities import consts
from Utilities.logger import Logger, LoggLevel


logger = Logger("[SCENARIO.RUNNER]", consts.ConfigVariables.DEFAULT_LOGS_INCUS.value)


def _now() -> datetime:
    return datetime.now(timezone.utc)


class ScenarioRunner:
    """Tracks scenario execution as an ordered list of steps.

    Usage:
        runner = ScenarioRunner("instance.provision", target=spec.name)
        async with runner.step("ensure_image") as step:
            fp = await ensure_image(...)
            step.detail["fingerprint"] = fp
        runner.finish(result={"name": spec.name})
        return runner.run
    """

    def __init__(self, scenario: str, target: str | None = None):
        self._run = ScenarioRun(
            id=str(uuid.uuid4()),
            scenario=scenario,
            target=target,
            status=StepStatus.RUNNING,
            started_at=_now(),
        )
        _store.put(self._run)
        target_part = f" target={target}" if target else ""
        logger.line(f"Run started scenario={scenario}{target_part} run_id={self._run.id}", LoggLevel.INFO)

    @property
    def run(self) -> ScenarioRun:
        return self._run

    @asynccontextmanager
    async def step(self, name: str):
        step = StepResult(name=name, status=StepStatus.RUNNING, started_at=_now())
        self._run.steps.append(step)
        logger.line(f"Step started run_id={self._run.id} step={name}", LoggLevel.INFO)
        try:
            yield step
        except Exception as exc:
            step.status = StepStatus.FAILED
            step.finished_at = _now()
            step.error = f"{type(exc).__name__}: {exc}"
            self._run.status = StepStatus.FAILED
            self._run.finished_at = _now()
            self._run.error = step.error
            logger.line(f"Step failed run_id={self._run.id} step={name} error={step.error}", LoggLevel.ERROR)
            raise
        else:
            step.status = StepStatus.DONE
            step.finished_at = _now()
            logger.line(f"Step done run_id={self._run.id} step={name}", LoggLevel.INFO)

    def skip(self, name: str, reason: str | None = None) -> None:
        self._run.steps.append(StepResult(
            name=name,
            status=StepStatus.SKIPPED,
            started_at=_now(),
            finished_at=_now(),
            detail={"reason": reason} if reason else {},
        ))
        reason_part = f" reason={reason}" if reason else ""
        logger.line(f"Step skipped run_id={self._run.id} step={name}{reason_part}", LoggLevel.INFO)

    def finish(self, result: dict[str, Any] | None = None) -> ScenarioRun:
        self._run.status = StepStatus.DONE
        self._run.finished_at = _now()
        self._run.result = result
        logger.line(f"Run finished scenario={self._run.scenario} run_id={self._run.id} status=done", LoggLevel.INFO)
        return self._run
