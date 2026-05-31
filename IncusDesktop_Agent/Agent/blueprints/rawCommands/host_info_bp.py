from flask import Blueprint
from Agent.controllers.agent.rawCommands.host_info import HostInfoController

raw_host_info_bp = Blueprint("host_info", __name__, url_prefix="/host/info")

def _ctrl() -> HostInfoController:
    return HostInfoController()

@raw_host_info_bp.get("/cpu")
async def cpu_info():
    return await _ctrl().cpu()