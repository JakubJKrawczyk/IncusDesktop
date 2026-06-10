"""Host info rawCommands — read-only host stats.

This category collects metrics and state descriptions of the host the
agent runs on. Endpoints here never mutate anything — pure READ.
GUI uses them for the dashboard, diagnostic panels, and preflight
checks before more expensive actions.

Everything runs through _executor.run with a fixed argv: /proc and
/sys files via the `cat` helper, other sources via their binaries
(lsblk, ip, uname, systemctl, journalctl, nvidia-smi, sensors, incus).
Raw stdout is parsed into tables with GlobalHelpers.StrHelper.parse_table.

Endpoints are grouped into three priority tiers — see sections below.
"""
import json
from tabnanny import check

from pydantic import Json

from Agent.controllers.agent.rawCommands._executor import CommandResult, run
from Utilities import consts
from Utilities.logger import Logger, LoggLevel
from Agent.exceptions import CommandFailedError, CommandTimeoutError
from general.helpers import GlobalHelpers


logger = Logger("[RAW.HOST_INFO]", consts.ConfigVariables.DEFAULT_LOGS_INCUS.value)


class HostInfoController:

    @staticmethod
    async def cat(path: str, timeout: float = 5):
        return (await run(["cat", path], timeout= timeout)).stdout

    async def cpu(self):
        """CPU info: model, cores, threads, clock, per-core %, loadavg.
        Sources: /proc/stat, /proc/cpuinfo, /proc/loadavg."""

        stat = (await run(["cat", "/proc/stat"], timeout=5)).stdout
        cpu_info = await HostInfoController.cat("/proc/cpuinfo")
        loadavg = await HostInfoController.cat("/proc/loadavg")

        # PROCESS STAT
        stat_table = GlobalHelpers.StrHelper.parse_table(stat)

        # PROCESS CPU INFO
        keys, values = [], []
        for l in cpu_info.splitlines():
            if not l.strip():
                continue
            if ":" not in l:
                continue
            key, value = l.split(":", 1)
            keys.append(key.strip())
            values.append(value.strip())

        cpu_info_table = {}
        for k,v in zip(keys, values):
            cpu_info_table[k]=v

        return {"cpu":{"stat":stat_table, "cpu_info":cpu_info_table, "loadavg":loadavg}}

    async def Memory(self):
        """RAM + swap: total/available/used/free/cached/buffers, swap*.
        Source: /proc/meminfo. Optionally top-N processes by RSS."""

        # PROCESS MEM INFO
        meminfo = await HostInfoController.cat("/proc/meminfo")

        meminfo_table = {}

        for l in meminfo.splitlines():
            key, value = l.split(":",1 )
            meminfo_table[key.strip()] = value.strip()

        return {"memory": meminfo_table}

    async def Disk(self):
        """Block devices + mounts: model, size, type (HDD/SSD/NVMe),
        per-mount used/free/fs/mountpoint. Incus storage pools listed
        in a separate section. Sources: lsblk -J, df, incus storage list."""

        lsblk = (await run(["lsblk", "-J"], timeout=5)).stdout
        df = (await run(["df", "-h"], timeout=5)).stdout

        lsblk = json.loads(lsblk)

        # PROCESS DF
        df_keys = df.splitlines()[0]
        df_keys = [l for l in df_keys.split(" ") if l != ""]
        df_dit = []
        for l in df.splitlines()[1:]:
            splitted = [x for x in l.split(" ") if x != ""]
            ob = {}
            for ll,k in zip(splitted, df_keys):
                if not ll.strip():
                    continue
                ll = ll.strip()
                ob[k]=ll
            df_dit.append(ob)

        return {"disk":{"lsblk":lsblk, "df":df_dit}}

    async def Network(self):
        """Network interfaces: per-iface rx/tx, errors, MTU, state,
        MAC, IPv4/v6. Incus bridges (incusbr0 etc.) in a separate section.
        Sources: /proc/net/dev, ip -j addr, ip -j link."""

        ip_addr = (await run(["ip", "-j", "addr"], timeout=5)).stdout
        ip_link = (await run(["ip", "-j", "link"], timeout=5)).stdout

        ip_addr_obj = json.loads(ip_addr)
        ip_link_obj = json.loads(ip_link)

        return {"network": {"addr":ip_addr_obj, "link":ip_link_obj}}

    async def Uptime(self):
        """Host uptime + OS info + kernel + hostname + arch.
        Sources: /proc/uptime, /etc/os-release, uname.
        Used mainly by the 'About this host' panel in the GUI."""

        uptime = await HostInfoController.cat("/proc/uptime")
        os_release = await HostInfoController.cat("/etc/os-release")
        uname = (await run(["uname", "-a"], timeout=5)).stdout

        # PROCESS OS RELEASE

        os_release_obj = {}
        for l in os_release.splitlines():
            k, v = l.split("=")
            k = k.strip()
            v = v.strip()

            os_release_obj[k] = v

        return {"uptime": {"uptime": uptime, "os_release": os_release_obj, "uname": uname}}

    async def Services(self):
        """Status of whitelisted systemd units: active/inactive/failed + enabled."""

        # PROCESS UNITS
        units = ["incus", "incus-startup", "incus.socket", "docker", "ssh"]
        result = {}
        for unit in units:
            active = (await run(["systemctl", "is-active", unit], ok_codes=(0,3,4))).stdout.strip()
            enabled = (await run(["systemctl", "is-enabled", unit], ok_codes=(0,1,4))).stdout.strip()
            result[unit] = {"active": active, "enabled": enabled}
        return result

    # ─── SHOULD HAVE (second sprint) ──────────────────────────────────────
    # Purpose: data for more detailed views — "Processes" tab,
    # "Incus overview" panel, troubleshooting. The user drills deeper
    # than the dashboard and wants to see what specifically is eating
    # the CPU, how many instances are in which state, what incus wrote
    # to the journal in the last 5 minutes. Not first-paint, but needed
    # when the user diagnoses or plans.

    async def Processes(self):
        """Top-N processes by CPU/RSS, optional name filter.
        Source: ps -eo pid,user,%cpu,%mem,rss,comm --sort=-%cpu."""
        pass

    async def IncusOverview(self):
        """Aggregate Incus state: version, instance counts per status
        (running/stopped/frozen), counts of projects/networks/pools/
        profiles, active operations. Cacheable for a few seconds — the
        dashboard polls this often."""
        pass

    async def Journal(self):
        """Structured logs from journald for whitelisted units
        (incus, docker). Params: unit, lines, since.
        Returns JSON entries (not raw text) — GUI renders them itself.
        Source: journalctl -u <unit> --no-pager -o json -n N."""
        pass

    # ─── NICE TO HAVE (when actually needed) ──────────────────────────────
    # Purpose: specialised info that not every host exposes and not every
    # user needs. GPU is critical for ML/rendering in Incus VMs with
    # passthrough; sensors help when the host is a physical machine and
    # someone cares about temperatures; runtime info for Docker/podman is
    # a preflight for the Docker workloads panel.
    # Everything optional and graceful — missing nvidia-smi must not crash
    # the response, only return {available: false}.

    async def Gpu(self):
        """GPU info (start: nvidia only): model, util%, temp,
        vram used/total, power draw, processes using GPU.
        Source: nvidia-smi --query-gpu=... --format=csv.
        AMD/Intel later."""
        pass

    async def Sensors(self):
        """Temperatures (CPU, NVMe, chipset), fan speeds, voltages.
        Source: sensors -j (lm-sensors).
        Often absent on servers without configuration — graceful degrade."""
        pass

    async def ContainersRuntime(self):
        """Detect and report status of docker/podman/k3s: version,
        daemon alive, container counts. Preflight before showing the
        Docker workloads panel in the GUI."""
        pass

    # ─── INTENTIONALLY OUT OF SCOPE ───────────────────────────────────────
    # Marks conscious "out of scope" decisions — so in a month nobody
    # comes back with "maybe let's add lspci" without remembering why it
    # was dropped. Each item below was considered and rejected for a
    # specific reason, not forgotten:
    #
    # - PCI/USB devices (lspci, lsusb) — rarely needed, easy to add later
    # - Firewall state (nft list, iptables -L) — large output, volatile
    #   format, low ROI for GUI
    # - DMI/SMBIOS (dmidecode) — requires root, low value for end user
    # - top/htop parsing — ps is enough, fewer moving parts
