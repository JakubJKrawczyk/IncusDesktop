# TODO — Pełne pokrycie Incus REST API (async)

Status: `[ ]` todo, `[x]` done, `[~]` in progress, `[!]` blocked

---

## Faza 0 — Migracja na async (prerekwizyt)
- [ ] Dodać `flask[async]` do `requirements.txt`
- [ ] Przepisać `utility/rest_client.py`: `httpx.AsyncClient` + wszystkie metody `async def` (`get/post/put/patch/delete/head/get_raw_with_headers/post_raw/delete_with_headers/_handle_envelope/_wait_operation/close`)
- [ ] Przepisać `controllers/instances.py` na `async def` (13 metod)
- [ ] Przepisać `controllers/instances_exec.py` na `async def` (10 metod)
- [ ] Przepisać `controllers/instances_files.py` na `async def` (4 metody + placeholder)
- [ ] Przepisać `blueprints/instances_bp.py` na `async def` (11 route'ów)
- [ ] Przepisać `blueprints/instancesExec_bp.py` na `async def` (10 route'ów)
- [ ] W `app.py` dodać shutdown hook: `atexit.register(lambda: asyncio.run(client.close()))`
- [ ] Smoke test: wszystkie 21 istniejących route'ów odpowiadają jak dotychczas (zero regresji)
- [ ] Test równoległości: 10×`curl /instances/<n>/state` w tle → czas ≈ 1× (nie 10×)

---

## Faza 1 — Dokończenie instances (~25 endpointów)

### Snapshots (`controllers/instances_snapshots.py`, `blueprints/instances_snapshots_bp.py`)
- [ ] `list_snapshots(name, recursion, project)` → `GET /1.0/instances/{name}/snapshots` (+`?recursion=1`)
- [ ] `create_snapshot(name, body, project)` → `POST /1.0/instances/{name}/snapshots` (async)
- [ ] `snapshot_info(name, snapshot, project)` → `GET /1.0/instances/{name}/snapshots/{snapshot}`
- [ ] `update_snapshot(name, snapshot, body, project)` → `PUT` (async)
- [ ] `patch_snapshot(name, snapshot, body, project)` → `PATCH` (204)
- [ ] `rename_snapshot(name, snapshot, body, project)` → `POST {snapshot}` (async)
- [ ] `delete_snapshot(name, snapshot, project)` → `DELETE` (async)
- [ ] Blueprint: 7 route'ów, prefix `/instances`, nazwa `instances_snapshots`
- [ ] Register w `app.py`

### Backups (`controllers/instances_backups.py`, `blueprints/instances_backups_bp.py`)
- [ ] `list_backups(name, recursion, project)` → `GET /1.0/instances/{name}/backups` (+`?recursion=1`)
- [ ] `create_backup(name, body, project)` → `POST` (async)
- [ ] `backup_info(name, backup, project)` → `GET /{backup}`
- [ ] `rename_backup(name, backup, new_name, project)` → `POST /{backup}` (async)
- [ ] `delete_backup(name, backup, project)` → `DELETE` (async)
- [ ] `export_backup(name, backup, project)` → `GET /{backup}/export` (raw) → `Response(mimetype="application/octet-stream")`
- [ ] Blueprint: 6 route'ów
- [ ] Register w `app.py`

### Metadata (`controllers/instances_metadata.py`, `blueprints/instances_metadata_bp.py`)
- [ ] `get_metadata(name, project)` → `GET /metadata`
- [ ] `update_metadata(name, body, project)` → `PUT /metadata`
- [ ] `patch_metadata(name, body, project)` → `PATCH /metadata` (204)
- [ ] `list_templates(name, project)` → `GET /metadata/templates` (bez `path`)
- [ ] `get_template(name, path, project)` → `GET /metadata/templates?path=` (raw)
- [ ] `put_template(name, path, content, project)` → `POST /metadata/templates?path=` (post_raw)
- [ ] `delete_template(name, path, project)` → `DELETE /metadata/templates?path=`
- [ ] Blueprint: rozgałęzienie `/metadata/templates` po obecności `path`
- [ ] Register w `app.py`

### Misc (`controllers/instances_misc.py`, `blueprints/instances_misc_bp.py`)
- [ ] `create_bitmap(name, body, project)` → `POST /bitmaps` (async)
- [ ] `debug_memory(name, format, project)` → `GET /debug/memory` (raw)
- [ ] `debug_repair(name, body, project)` → `GET /debug/repair`
- [ ] Blueprint: 3 route'y
- [ ] Register w `app.py`

### Modele
- [ ] `InstanceMetadata` w `models/instance_model.py` (architecture, creation_date, expiry_date, properties, templates)

### Smoke
- [ ] `curl /instances/<n>/snapshots?recursion=1`, `POST /snapshots`, `GET /backups/<b>/export`, `GET /metadata`, `GET /debug/memory -o mem.elf`

---

## Faza 2 — Images (17 endpointów, PRIORYTET)

### `controllers/images.py`
- [ ] `list_images(recursion, public, project, filter, all_projects)` → `GET /1.0/images` (+`?public`/`?recursion=1/2`)
- [ ] `create_image(body, project)` → `POST /1.0/images` (JSON, async)
- [ ] `upload_image(content, headers, project)` → `POST /1.0/images` (octet-stream/multipart, post_raw, async)
- [ ] `image_info(fingerprint, public, project)` → `GET /{fp}` (+`?public`)
- [ ] `update_image(fingerprint, body, project)` → `PUT /{fp}`
- [ ] `patch_image(fingerprint, body, project)` → `PATCH /{fp}` (204)
- [ ] `delete_image(fingerprint, project)` → `DELETE /{fp}` (async)
- [ ] `export_image(fingerprint, public, project)` → `GET /{fp}/export` (raw, +`?public`)
- [ ] `push_export_image(fingerprint, body, project)` → `POST /{fp}/export` (async)
- [ ] `refresh_image(fingerprint, project)` → `POST /{fp}/refresh` (async)
- [ ] `create_image_secret(fingerprint, project)` → `POST /{fp}/secret` (async)
- [ ] `list_aliases(recursion, project)` → `GET /aliases` (+`?recursion=1`)
- [ ] `create_alias(body, project)` → `POST /aliases`
- [ ] `alias_info(name, public, project)` → `GET /aliases/{name}` (+`?public`)
- [ ] `update_alias(name, body, project)` → `PUT /aliases/{name}`
- [ ] `patch_alias(name, body, project)` → `PATCH /aliases/{name}` (204)
- [ ] `rename_alias(name, new_name, project)` → `POST /aliases/{name}`
- [ ] `delete_alias(name, project)` → `DELETE /aliases/{name}`

### `blueprints/images_bp.py`
- [ ] `Blueprint("images", __name__, url_prefix="/images")`
- [ ] Kolejność routów: **statyczne `/aliases*` przed dynamicznym `/<fingerprint>`**
- [ ] `POST ""` dispatcher po `request.content_type` (JSON → `create_image`, inne → `upload_image` z wyłuskanymi `X-Incus-*` headers)
- [ ] Export: `Response(data, mimetype="application/octet-stream")`

### Modele (`models/image_model.py`)
- [ ] `ImageModel` (fingerprint, aliases, auto_update, cached, created_at, expires_at, filename, fingerprint, last_used_at, architecture, profiles, properties, public, size, type, uploaded_at, update_source, project)
- [ ] `ImageAliasModel` (name, description, target, type)
- [ ] `ImageSource` (alias, certificate, fingerprint, mode, protocol, secret, server, type, url)
- [ ] `ImageMetadata` (architecture, creation_date, expiry_date, properties, templates) — współdzielony z instances metadata

### Register + smoke
- [ ] Register `images_bp` w `app.py`
- [ ] `curl /images?recursion=1`, `curl /images/<fp>`, `curl -o img.tar /images/<fp>/export`, upload `curl -X POST --data-binary @img.tar -H 'Content-Type: application/octet-stream' /images`

---

## Faza 3 — Server / meta / warnings (10 endpointów)

### `controllers/server.py`
- [ ] `root()` → `GET /`
- [ ] `server_info(public)` → `GET /1.0` (+`?public`)
- [ ] `update_server(body)` → `PUT /1.0`
- [ ] `patch_server(body)` → `PATCH /1.0` (204)
- [ ] `events_stream(type, project)` → `GET /1.0/events` (**placeholder 501**, WebSocket)
- [ ] `resources()` → `GET /1.0/resources`
- [ ] `metrics(project)` → `GET /1.0/metrics` (raw text)
- [ ] `metadata_configuration()` → `GET /1.0/metadata/configuration`

### `controllers/warnings.py`
- [ ] `list_warnings(recursion, project)` → `GET /1.0/warnings` (+`?recursion=1`)
- [ ] `warning_info(uuid)` → `GET /{uuid}`
- [ ] `update_warning(uuid, body)` → `PUT /{uuid}`
- [ ] `delete_warning(uuid)` → `DELETE /{uuid}`

### Blueprinty + modele
- [ ] `blueprints/server_bp.py` (prefix `""`, route `/server` dla `/1.0`, `/events` → 501, `/metrics` → `Response(mimetype="text/plain; version=0.0.4")`, `/resources`, `/metadata/configuration`, `/`)
- [ ] `blueprints/warnings_bp.py` (prefix `/warnings`)
- [ ] `models/server_model.py` (`ServerModel`, `ServerEnvironment`)
- [ ] `models/resources_model.py` (`ResourcesModel`)
- [ ] `models/warning_model.py` (`WarningModel`)

### Register + smoke
- [ ] Register `server_bp`, `warnings_bp`
- [ ] `curl /server`, `/resources`, `/warnings?recursion=1`

---

## Faza 4 — Profiles + Projects (11 endpointów)

### `controllers/profiles.py`
- [ ] `list_profiles(recursion, project, filter)` → `GET /1.0/profiles` (+`?recursion=1`)
- [ ] `create_profile(body, project)` → `POST`
- [ ] `profile_info(name, project)` → `GET /{name}`
- [ ] `update_profile(name, body, project)` → `PUT /{name}`
- [ ] `patch_profile(name, body, project)` → `PATCH /{name}` (204)
- [ ] `rename_profile(name, new_name, project)` → `POST /{name}`
- [ ] `delete_profile(name, project)` → `DELETE /{name}`

### `controllers/projects.py`
- [ ] `list_projects(recursion, filter)` → `GET /1.0/projects` (+`?recursion=1`)
- [ ] `create_project(body)` → `POST`
- [ ] `project_info(name)` → `GET /{name}`
- [ ] `update_project(name, body)` → `PUT /{name}`
- [ ] `patch_project(name, body)` → `PATCH /{name}` (204)
- [ ] `rename_project(name, new_name)` → `POST /{name}` (async)
- [ ] `delete_project(name)` → `DELETE /{name}`
- [ ] `project_access(name)` → `GET /{name}/access` → `Access`
- [ ] `project_state(name)` → `GET /{name}/state` → `ProjectState`

### Blueprinty + modele + register
- [ ] `blueprints/profiles_bp.py` (prefix `/profiles`)
- [ ] `blueprints/projects_bp.py` (prefix `/projects`)
- [ ] `models/profile_model.py` (`ProfileModel`)
- [ ] `models/project_model.py` (`ProjectModel`, `ProjectState`)
- [ ] Register + smoke: `curl /profiles?recursion=1`, `/projects/default/state`

---

## Faza 5 — Networks core (26 endpointów)

### `controllers/networks.py`
- [ ] `list_networks(recursion, project, all_projects)` → `GET /1.0/networks` (+`?recursion=1`)
- [ ] `create_network(body, project)` → `POST`
- [ ] `network_info(name, project)` → `GET /{name}`
- [ ] `update_network(name, body, project)` → `PUT /{name}`
- [ ] `patch_network(name, body, project)` → `PATCH /{name}` (204)
- [ ] `rename_network(name, new_name, project)` → `POST /{name}`
- [ ] `delete_network(name, project)` → `DELETE /{name}`
- [ ] `network_leases(name, project)` → `GET /{name}/leases`
- [ ] `network_state(name, project)` → `GET /{name}/state`

### `controllers/networks_forwards.py`
- [ ] `list_forwards(network, recursion, project)` → `GET /networks/{network}/forwards` (+`?recursion=1`)
- [ ] `create_forward(network, body, project)` → `POST`
- [ ] `forward_info(network, listen_address, project)` → `GET /{listenAddress}`
- [ ] `update_forward` → `PUT`
- [ ] `patch_forward` → `PATCH` (204)
- [ ] `delete_forward` → `DELETE`

### `controllers/networks_load_balancers.py`
- [ ] Jak forwards + `load_balancer_state(network, listen_address, project)` → `GET /{listenAddress}/state`

### `controllers/networks_peers.py`
- [ ] `list_peers(recursion)`, `create_peer`, `peer_info({peerName})`, `update_peer`, `patch_peer`, `delete_peer`

### Blueprinty + modele + register
- [ ] 4 blueprinty z prefix `/networks` i unikalnymi nazwami (`networks`, `networks_forwards`, `networks_load_balancers`, `networks_peers`)
- [ ] `models/network_model.py`: `NetworkModel`, `NetworkState`, `NetworkLease`, `NetworkForward`, `NetworkForwardPort`, `NetworkLoadBalancer`, `NetworkLoadBalancerState`, `NetworkPeer`
- [ ] Register wszystkich 4
- [ ] Smoke: `curl /networks?recursion=1`, `/networks/incusbr0/leases`, `/networks/incusbr0/forwards`

---

## Faza 6 — Network accessories (22 endpointy)
- [ ] `controllers/network_acls.py` — CRUD + rename + `acl_log` (raw text)
- [ ] `controllers/network_address_sets.py` — CRUD + rename
- [ ] `controllers/network_allocations.py` — `list_allocations(project, all_projects)`
- [ ] `controllers/network_integrations.py` — CRUD + rename
- [ ] `controllers/network_zones.py` — CRUD
- [ ] `controllers/network_zones_records.py` — CRUD na `/network-zones/{zone}/records[/{name}]`
- [ ] 6 blueprintów (unikalne nazwy)
- [ ] Modele: `network_acl_model.py`, `network_address_set_model.py`, `network_allocation_model.py`, `network_integration_model.py`, `network_zone_model.py`
- [ ] Register + smoke: `curl /network-acls?recursion=1`, `/network-zones`, `/network-allocations`

---

## Faza 7 — Storage (~40 endpointów)

### Core
- [ ] `controllers/storage_pools.py` — CRUD + `pool_resources` → `/resources`
- [ ] `controllers/storage_volumes.py` — list (z/bez `{type}`, `recursion 1/2`), CRUD, rename(async), `volume_state`, `volume_nbd`/`volume_sftp` (**placeholdery 101**), `import_volume_from_backup` (octet-stream → post_raw)

### Sub-resources
- [ ] `controllers/storage_volumes_snapshots.py`
- [ ] `controllers/storage_volumes_backups.py` (+ `export` raw)
- [ ] `controllers/storage_volumes_bitmaps.py`
- [ ] `controllers/storage_volumes_files.py` (wzór `instances_files.py`)
- [ ] `controllers/storage_buckets.py`
- [ ] `controllers/storage_buckets_keys.py`
- [ ] `controllers/storage_buckets_backups.py` (+ `export` raw)

### Blueprinty + model + register
- [ ] 9 blueprintów z prefix `/storage-pools` (unikalne nazwy)
- [ ] `models/storage_model.py` — `StoragePoolModel`, `StoragePoolResources`, `StorageVolumeModel`, `StorageVolumeState`, `StorageVolumeSnapshot`, `StorageVolumeBackup`, `StorageVolumeBitmap`, `StorageBucketModel`, `StorageBucketKey`, `StorageBucketBackup`
- [ ] Register wszystkich 9
- [ ] Smoke: `curl /storage-pools?recursion=1`, `/storage-pools/default/volumes?recursion=2`, `/storage-pools/default/buckets`

---

## Faza 8 — Cluster + Certificates + Operations (~20 endpointów)

### `controllers/cluster.py`
- [ ] `cluster_info` → `GET /1.0/cluster`
- [ ] `update_cluster(body)` → `PUT` (async)
- [ ] `cluster_certificate(body)` → `PUT /certificate`
- [ ] Groups CRUD+rename (`list_groups(recursion)`, `create_group`, `group_info`, `update_group`, `patch_group`, `rename_group`, `delete_group`)
- [ ] Members CRUD+rename+join token + state+action (`list_members(recursion)`, `request_join_token`, `member_info`, `update_member`, `patch_member`, `rename_member`, `delete_member(force)`, `member_state`, `member_state_action` async)

### `controllers/certificates.py`
- [ ] `list_certificates(recursion, public)` → `GET /1.0/certificates`
- [ ] `create_certificate(body, public)` → `POST`
- [ ] `certificate_info(fingerprint)` → `GET /{fp}`
- [ ] `update_certificate(fingerprint, body)` → `PUT /{fp}`
- [ ] `patch_certificate(fingerprint, body)` → `PATCH /{fp}` (204)
- [ ] `delete_certificate(fingerprint)` → `DELETE /{fp}`

### `controllers/operations.py`
- [ ] `list_operations(recursion, project, all_projects)` → `GET /1.0/operations`
- [ ] `operation_info(id)` → `GET /{id}`
- [ ] `cancel_operation(id)` → `DELETE /{id}`
- [ ] `wait_operation(id, timeout, public)` → `GET /{id}/wait`
- [ ] `operation_websocket(id, secret, public)` → `GET /{id}/websocket` (**placeholder 501**)

### Blueprinty + modele + register
- [ ] `blueprints/cluster_bp.py` (`/cluster`)
- [ ] `blueprints/certificates_bp.py` (`/certificates`)
- [ ] `blueprints/operations_bp.py` (`/operations`)
- [ ] `models/cluster_model.py` (`ClusterInfo`, `ClusterMember`, `ClusterMemberState`, `ClusterGroup`)
- [ ] `models/certificate_model.py` (`CertificateModel`)
- [ ] Register wszystkich 3
- [ ] Smoke: `curl /cluster`, `/operations?recursion=1`, `/certificates?recursion=1`

---

## Definition of Done (globalne)
- [ ] Wszystkie 151 endpointów z `rest-api.yaml` zaimplementowane lub jawnie oznaczone jako placeholder 501 (WebSocket/SFTP/NBD)
- [ ] Wszystkie route'y odpowiadają kształtem envelope'a identycznie do daemona Incusa
- [ ] Testy kontraktowe w `tests/` z `httpx.MockTransport` dla każdej metody kontrolera (happy-path)
- [ ] Async I/O zweryfikowane: 10 równoległych wywołań z klienta trwa ≈ 1 zapytanie, nie 10
