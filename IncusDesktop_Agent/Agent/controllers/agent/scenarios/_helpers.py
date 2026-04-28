"""Shared async building blocks for scenarios.

Each helper performs an idempotent ensure_*-style action against the Incus
daemon, or wraps a non-trivial poll. Helpers return primitive data
(strings/bools) — they don't manipulate ScenarioRun state directly. The
calling scenario records what it wants in step.detail.
"""
import asyncio
from logging import INFO
from typing import Any

from Agent.controllers.incus.images import ImagesController
from Agent.controllers.incus.instances import InstancesController
from Agent.controllers.incus.instances_snapshots import InstancesSnapshotsController
from Agent.controllers.incus.networks import NetworksController
from Agent.controllers.incus.networks_forwards import NetworksForwardsController
from Agent.controllers.incus.profiles import ProfilesController
from Agent.controllers.incus.storage_pools import StoragePoolsController
from Agent.controllers.incus.storage_volumes import StorageVolumesController
from Agent.utility.rest_client import IncusError, IncusRestClient
from Utilities import consts
from Utilities.logger import Logger, LoggLevel

# ─── Images ────────────────────────────────────────────────────────────────

logger = Logger("[INCUS.HELPERS]", consts.ConfigVariables.DEFAULT_LOGS_INCUS.value)

async def ensure_image(
    client: IncusRestClient,
    alias: str,
    *,
    server: str = "https://images.linuxcontainers.org",
    protocol: str = "simplestreams",
    project: str = "default",
) -> str:
    """Returns fingerprint of an image with the given local alias.

    If the alias is not present locally, pulls the image from `server`,
    waits for the pull operation, then registers the alias pointing at
    the fetched fingerprint.
    """
    images = ImagesController(client)
    logger.line(f"Checking for image existence alias={alias} project={project}", LoggLevel.INFO)
    try:
        alias_info = await images.alias_info(alias, project=project)
        target = alias_info.get("target") if isinstance(alias_info, dict) else getattr(alias_info, "target", None)
        if target:
            logger.line(f"Target image found alias={alias} fingerprint={target}", LoggLevel.INFO)
            return target
    except IncusError:
        logger.line(f"Image alias not present locally alias={alias}", LoggLevel.INFO)

    logger.line(f"Pulling image alias={alias} server={server} protocol={protocol}", LoggLevel.INFO)
    op_metadata = await images.create_image(
        body={
            "source": {
                "type": "image",
                "mode": "pull",
                "server": server,
                "protocol": protocol,
                "alias": alias,
            },
        },
        project=project,
    )

    fingerprint = _extract_fingerprint(op_metadata)
    if not fingerprint:
        logger.line(f"Image pull yielded no fingerprint alias={alias}", LoggLevel.ERROR)
        raise IncusError(f"image pull for alias {alias!r} did not yield a fingerprint")
    logger.line(f"Image pulled alias={alias} fingerprint={fingerprint}", LoggLevel.INFO)

    try:
        await images.create_alias(
            body={"name": alias, "target": fingerprint},
            project=project,
        )
        logger.line(f"Image alias registered alias={alias} fingerprint={fingerprint}", LoggLevel.INFO)
    except IncusError as exc:
        logger.line(f"Image alias registration skipped (race or already exists) alias={alias} error={exc}", LoggLevel.WARNING)

    return fingerprint


def _extract_fingerprint(op_metadata: Any) -> str | None:
    if not isinstance(op_metadata, dict):
        return None
    if fp := op_metadata.get("fingerprint"):
        return fp
    inner = op_metadata.get("metadata")
    if isinstance(inner, dict) and (fp := inner.get("fingerprint")):
        return fp
    return None


# ─── Networks ──────────────────────────────────────────────────────────────

async def ensure_network(
    client: IncusRestClient,
    name: str,
    *,
    type: str = "bridge",
    config: dict[str, Any] | None = None,
    project: str = "default",
) -> bool:
    """Returns True if the network was created, False if it already existed."""
    networks = NetworksController(client)
    logger.line(f"Checking network existence name={name} project={project}", LoggLevel.INFO)
    try:
        await networks.network_info(name, project=project)
        logger.line(f"Network already exists name={name}", LoggLevel.INFO)
        return False
    except IncusError:
        pass

    logger.line(f"Creating network name={name} type={type}", LoggLevel.INFO)
    await networks.create_network(
        body={"name": name, "type": type, "config": config or {}},
        project=project,
    )
    logger.line(f"Network created name={name}", LoggLevel.INFO)
    return True


async def ensure_network_forward(
    client: IncusRestClient,
    network: str,
    listen_address: str,
    *,
    ports: list[dict[str, Any]] | None = None,
    description: str | None = None,
    project: str = "default",
) -> bool:
    """Ensure a network forward exists at listen_address. Ports list shape:
    [{"protocol": "tcp", "listen_port": "8080", "target_port": "80",
      "target_address": "10.0.0.5"}, ...]
    """
    forwards = NetworksForwardsController(client)
    logger.line(f"Checking network forward existence network={network} listen={listen_address}", LoggLevel.INFO)
    try:
        await forwards.forward_info(network, listen_address, project=project)
        logger.line(f"Network forward already exists network={network} listen={listen_address}", LoggLevel.INFO)
        return False
    except IncusError:
        pass

    body: dict[str, Any] = {"listen_address": listen_address, "ports": ports or []}
    if description is not None:
        body["description"] = description
    logger.line(f"Creating network forward network={network} listen={listen_address} ports={len(body['ports'])}", LoggLevel.INFO)
    await forwards.create_forward(network, body=body, project=project)
    logger.line(f"Network forward created network={network} listen={listen_address}", LoggLevel.INFO)
    return True


# ─── Storage ───────────────────────────────────────────────────────────────

async def ensure_storage_pool(
    client: IncusRestClient,
    name: str,
    *,
    driver: str = "dir",
    config: dict[str, Any] | None = None,
) -> bool:
    pools = StoragePoolsController(client)
    logger.line(f"Checking storage pool existence name={name}", LoggLevel.INFO)
    try:
        await pools.pool_info(name)
        logger.line(f"Storage pool already exists name={name}", LoggLevel.INFO)
        return False
    except IncusError:
        pass

    logger.line(f"Creating storage pool name={name} driver={driver}", LoggLevel.INFO)
    await pools.create_pool(body={"name": name, "driver": driver, "config": config or {}})
    logger.line(f"Storage pool created name={name}", LoggLevel.INFO)
    return True


async def ensure_storage_volume(
    client: IncusRestClient,
    pool: str,
    name: str,
    *,
    type: str = "custom",
    size: str | None = None,
    config: dict[str, Any] | None = None,
    project: str = "default",
) -> bool:
    volumes = StorageVolumesController(client)
    logger.line(f"Checking storage volume existence pool={pool} name={name} type={type}", LoggLevel.INFO)
    try:
        await volumes.volume_info(pool, type, name, project=project)
        logger.line(f"Storage volume already exists pool={pool} name={name}", LoggLevel.INFO)
        return False
    except IncusError:
        pass

    vol_config = dict(config or {})
    if size:
        vol_config.setdefault("size", size)

    logger.line(f"Creating storage volume pool={pool} name={name} size={size}", LoggLevel.INFO)
    await volumes.create_volume(
        pool=pool,
        body={"name": name, "type": type, "config": vol_config},
        project=project,
    )
    logger.line(f"Storage volume created pool={pool} name={name}", LoggLevel.INFO)
    return True


# ─── Profiles ──────────────────────────────────────────────────────────────

async def ensure_profile(
    client: IncusRestClient,
    name: str,
    *,
    config: dict[str, Any] | None = None,
    devices: dict[str, dict[str, Any]] | None = None,
    description: str | None = None,
    project: str = "default",
) -> bool:
    profiles = ProfilesController(client)
    logger.line(f"Checking profile existence name={name} project={project}", LoggLevel.INFO)
    try:
        await profiles.profile_info(name, project=project)
        logger.line(f"Profile already exists name={name}", LoggLevel.INFO)
        return False
    except IncusError:
        pass

    body: dict[str, Any] = {
        "name": name,
        "config": config or {},
        "devices": devices or {},
    }
    if description is not None:
        body["description"] = description
    logger.line(f"Creating profile name={name} project={project}", LoggLevel.INFO)
    await profiles.create_profile(body=body, project=project)
    logger.line(f"Profile created name={name}", LoggLevel.INFO)
    return True


# ─── Instance state polling ────────────────────────────────────────────────

async def wait_agent_ready(
    client: IncusRestClient,
    name: str,
    *,
    project: str = "default",
    timeout: int = 120,
    poll_interval: float = 1.5,
) -> bool:
    """Poll instance state until it has a non-loopback IPv4/IPv6 address.

    Returns True when ready, False on timeout. We treat "first non-loopback
    IP" as a reasonable proxy for "guest agent reachable" — works for both
    container (lxc) and VM (incus-agent) cases.
    """
    instances = InstancesController(client)
    deadline = asyncio.get_event_loop().time() + timeout
    logger.line(f"Waiting for agent ready name={name} timeout={timeout}s", LoggLevel.INFO)

    while asyncio.get_event_loop().time() < deadline:
        try:
            state = await instances.instance_state(name, project=project)
        except IncusError:
            await asyncio.sleep(poll_interval)
            continue

        if _state_has_nonlocal_address(state):
            logger.line(f"Agent ready name={name}", LoggLevel.INFO)
            return True
        await asyncio.sleep(poll_interval)

    logger.line(f"Agent not ready within timeout name={name} timeout={timeout}s", LoggLevel.WARNING)
    return False


def _state_has_nonlocal_address(state: Any) -> bool:
    network = state.get("network") if isinstance(state, dict) else getattr(state, "network", None)
    if not network:
        return False
    for iface_name, iface in network.items() if isinstance(network, dict) else []:
        if iface_name == "lo":
            continue
        addresses = iface.get("addresses") if isinstance(iface, dict) else None
        if not addresses:
            continue
        for addr in addresses:
            if not isinstance(addr, dict):
                continue
            address = addr.get("address", "")
            scope = addr.get("scope", "")
            if not address or address.startswith("127.") or address == "::1":
                continue
            if scope and scope != "global" and scope != "link":
                continue
            return True
    return False


# ─── Snapshot retention ────────────────────────────────────────────────────

async def prune_old_snapshots(
    client: IncusRestClient,
    instance: str,
    *,
    keep_last_n: int,
    project: str = "default",
) -> list[str]:
    """Keep `keep_last_n` most recent snapshots, delete the rest. Returns
    list of deleted snapshot names."""
    snapshots_ctrl = InstancesSnapshotsController(client)
    logger.line(f"Pruning old snapshots instance={instance} keep_last_n={keep_last_n}", LoggLevel.INFO)
    snaps = await snapshots_ctrl.list_snapshots(instance, recursion=1, project=project)

    if not isinstance(snaps, list) or len(snaps) <= keep_last_n:
        logger.line(f"No snapshots to prune instance={instance} count={len(snaps) if isinstance(snaps, list) else 0}", LoggLevel.INFO)
        return []

    def _key(s):
        if isinstance(s, dict):
            return s.get("created_at") or s.get("name") or ""
        return getattr(s, "created_at", None) or getattr(s, "name", "") or ""

    sorted_snaps = sorted(snaps, key=_key, reverse=True)
    to_delete = sorted_snaps[keep_last_n:]

    deleted: list[str] = []
    for snap in to_delete:
        snap_name = snap.get("name") if isinstance(snap, dict) else getattr(snap, "name", None)
        if not snap_name:
            continue
        try:
            await snapshots_ctrl.delete_snapshot(instance, snap_name, project=project)
            deleted.append(snap_name)
        except IncusError as exc:
            logger.line(f"Failed to delete snapshot instance={instance} snapshot={snap_name} error={exc}", LoggLevel.WARNING)
    logger.line(f"Pruned snapshots instance={instance} deleted={len(deleted)}", LoggLevel.INFO)
    return deleted


# ─── Cloud-init / ssh injection ────────────────────────────────────────────

def build_cloud_init_user_data(
    *,
    ssh_pubkey: str | None = None,
    extra_user_data: str | None = None,
) -> str:
    """Compose a #cloud-config document with optional ssh key. If
    extra_user_data is provided it is appended verbatim under the same
    document; caller is responsible for valid YAML.
    """
    lines = ["#cloud-config"]
    if ssh_pubkey:
        lines.append("ssh_authorized_keys:")
        lines.append(f"  - {ssh_pubkey.strip()}")
    if extra_user_data:
        stripped = extra_user_data.lstrip()
        if stripped.startswith("#cloud-config"):
            stripped = stripped.split("\n", 1)[1] if "\n" in stripped else ""
        lines.append(stripped)
    return "\n".join(lines) + "\n"


# ─── Operation result extraction ───────────────────────────────────────────

def operation_metadata(op: Any) -> dict[str, Any]:
    """The rest client auto-waits operations and returns the inner metadata
    dict; this helper normalizes whatever shape is returned to a dict."""
    if isinstance(op, dict):
        return op
    if hasattr(op, "model_dump"):
        return op.model_dump()
    return {}
