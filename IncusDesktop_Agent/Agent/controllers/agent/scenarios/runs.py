from Agent.controllers.agent.scenarios import _store
from Agent.models.scenarios.runs import ScenarioRun
from Utilities import consts
from Utilities.logger import Logger, LoggLevel


logger = Logger("[SCENARIO.RUNS]", consts.ConfigVariables.DEFAULT_LOGS_INCUS.value)


class RunsController:
    """Read-only access to the in-process scenario run store."""

    # GET /scenarios/runs
    async def list_runs(self) -> list[ScenarioRun]:
        runs = _store.list_all()
        logger.line(f"List runs count={len(runs)}", LoggLevel.INFO)
        return runs

    # GET /scenarios/runs/{id}
    async def get_run(self, run_id: str) -> ScenarioRun | None:
        run = _store.get(run_id)
        if run is None:
            logger.line(f"Get run not found run_id={run_id}", LoggLevel.WARNING)
        else:
            logger.line(f"Get run run_id={run_id} status={run.status}", LoggLevel.INFO)
        return run

    # DELETE /scenarios/runs/{id}
    async def delete_run(self, run_id: str) -> bool:
        deleted = _store.delete(run_id)
        if deleted:
            logger.line(f"Run deleted run_id={run_id}", LoggLevel.INFO)
        else:
            logger.line(f"Delete run not found run_id={run_id}", LoggLevel.WARNING)
        return deleted
