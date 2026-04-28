from dataclasses import asdict

from flask import Blueprint, jsonify

from Agent.controllers.agent.rawCommands.examples import ExamplesController


bp = Blueprint("raw_examples", __name__, url_prefix="/raw")


def _ctrl() -> ExamplesController:
    return ExamplesController()


@bp.post("/echo")
async def echo_dupa():
    result = await _ctrl().echo_dupa()
    status = 200 if result.return_code == 0 and not result.timed_out else 500
    return jsonify(asdict(result)), status
