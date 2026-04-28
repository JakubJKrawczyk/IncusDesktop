from Agent.models.scenarios.runs import ScenarioRun


_runs: dict[str, ScenarioRun] = {}


def put(run: ScenarioRun) -> None:
    _runs[run.id] = run


def get(run_id: str) -> ScenarioRun | None:
    return _runs.get(run_id)


def list_all() -> list[ScenarioRun]:
    return list(_runs.values())


def delete(run_id: str) -> bool:
    return _runs.pop(run_id, None) is not None
