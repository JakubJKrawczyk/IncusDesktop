"""Host info rawCommands — read-only host stats.

This category collects metrics and state descriptions of the host the
agent runs on. Endpoints here never mutate anything — pure READ.
GUI uses them for the dashboard, diagnostic panels, and preflight
checks before more expensive actions.

Anything readable from /proc or /sys goes through Python open() —
no shelling out to `cat`. Only binaries that cannot be replaced
(lsblk, ip, systemctl, journalctl, nvidia-smi, sensors) are invoked
via _executor.run with a fixed argv.

Every response includes `collected_at` (UTC timestamp) so the GUI
can cache and decide when to refresh.

Endpoints are grouped into three priority tiers — see sections below.
"""
from Agent.controllers.agent.rawCommands._executor import CommandResult, run
from Utilities import consts
from Utilities.logger import Logger, LoggLevel
from Agent.exceptions import CommandFailedError, CommandTimeoutError


logger = Logger("[RAW.HOST_INFO]", consts.ConfigVariables.DEFAULT_LOGS_INCUS.value)


class HostInfoController:


    async def cpu(self):
        """CPU info: model, cores, threads, clock, per-core %, loadavg.
        Sources: /proc/stat, /proc/cpuinfo, /proc/loadavg."""

        results = await run(["cat", "/proc/stat", "|", "grep", "cpu"], timeout=5)

        if results.stderr is None:
            return results.stdout
        else:
            raise CommandFailedError("")
        return

    async def Memory(self):
        """RAM + swap: total/available/used/free/cached/buffers, swap*.
        Source: /proc/meminfo. Optionally top-N processes by RSS."""
        pass

    async def Disk(self):
        """Block devices + mounts: model, size, type (HDD/SSD/NVMe),
        per-mount used/free/fs/mountpoint. Incus storage pools listed
        in a separate section. Sources: lsblk -J, df, incus storage list."""
        pass

    async def Network(self):
        """Network interfaces: per-iface rx/tx, errors, MTU, state,
        MAC, IPv4/v6. Incus bridges (incusbr0 etc.) in a separate section.
        Sources: /proc/net/dev, ip -j addr, ip -j link."""
        pass

    async def Uptime(self):
        """Host uptime + OS info + kernel + hostname + arch.
        Sources: /proc/uptime, /etc/os-release, uname.
        Used mainly by the 'About this host' panel in the GUI."""
        pass

    async def Services(self):
        """Status of whitelisted systemd units (incus, incus-startup,
        incus.socket, docker, ssh): active/inactive/failed + enabled.
        Source: systemctl is-active / is-enabled."""
        pass

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
