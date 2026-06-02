from flask import Blueprint
from Agent.controllers.agent.rawCommands.host_info import HostInfoController

raw_host_info_bp = Blueprint("host_info", __name__, url_prefix="/host/info")

def _ctrl() -> HostInfoController:
    return HostInfoController()

# ─── MUST HAVE (dashboard, first paint) ───────────────────────────────

@raw_host_info_bp.get("/cpu")
async def cpu_info():
    return await _ctrl().cpu()

@raw_host_info_bp.get("/memory")
async def memory_info():
    return await _ctrl().Memory()

@raw_host_info_bp.get("/disk")
async def disk_info():
    return await _ctrl().Disk()

@raw_host_info_bp.get("/network")
async def network_info():
    return await _ctrl().Network()

@raw_host_info_bp.get("/uptime")
async def uptime_info():
    return await _ctrl().Uptime()

@raw_host_info_bp.get("/services")
async def services_info():
    return await _ctrl().Services()

# ─── SHOULD HAVE (detailed views, troubleshooting) ────────────────────

@raw_host_info_bp.get("/processes")
async def processes_info():
    return await _ctrl().Processes()

@raw_host_info_bp.get("/incus")
async def incus_overview():
    return await _ctrl().IncusOverview()

@raw_host_info_bp.get("/journal")
async def journal_info():
    return await _ctrl().Journal()

# ─── NICE TO HAVE (hardware-specific, graceful degrade) ───────────────

@raw_host_info_bp.get("/gpu")
async def gpu_info():
    return await _ctrl().Gpu()

@raw_host_info_bp.get("/sensors")
async def sensors_info():
    return await _ctrl().Sensors()

@raw_host_info_bp.get("/containers-runtime")
async def containers_runtime_info():
    return await _ctrl().ContainersRuntime()
