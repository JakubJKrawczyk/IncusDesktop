# Plan pełnego pokrycia Incus REST API (async)

## Context
`rest-api.yaml` to OpenAPI spec Incusa (18177 linii, 151 endpointów). Projekt aktualnie pokrywa ~14% (21 route'ów): core instances, exec/console/logs, częściowo files. Cel: zaimplementować pozostałe **130 endpointów** w 9 fazach, z **Images jako priorytetem** zaraz po dokończeniu domeny instances.

**Dodatkowy cel: async.** Przechodzimy z `httpx.Client` na `httpx.AsyncClient` + `async def` route'y w Flasku, żeby klient mógł robić wiele operacji równolegle (bulk calls, równoległe fetch stanów wielu instancji, itd.).

Reguła nadrzędna: **w istniejącym wzorcu**, bez DTO/service layerów/base-klas/DI. Tylko zamieniamy sync → async.

---

## Wzorzec async (nowy — zamrożony, powielać 1:1)

### REST client (`utility/rest_client.py`) — przepisany na async
```python
import httpx

class IncusRestClient:
    DEFAULT_SOCKET = "/var/lib/incus/unix.socket"

    def __init__(self, socket_path=DEFAULT_SOCKET, timeout=30.0):
        transport = httpx.AsyncHTTPTransport(uds=socket_path)
        self._client = httpx.AsyncClient(transport=transport, timeout=timeout,
                                         base_url="http://localhost",
                                         headers={"Content-Type": "application/json"})

    async def close(self): await self._client.aclose()

    async def get(self, path, params=None, *, raw=False): ...
    async def post(self, path, json_body=None, *, params=None, wait=True, wait_timeout=60): ...
    async def put(...): ...
    async def patch(...): ...
    async def delete(...): ...
    async def head(...): ...
    async def get_raw_with_headers(...): ...
    async def post_raw(...): ...
    async def delete_with_headers(...): ...

    async def _request(self, method, path, *, params=None, json_body=None,
                       wait=True, wait_timeout=60, raw=False):
        try:
            response = await self._client.request(method, path, params=params, json=json_body)
        except httpx.RequestError as exc:
            raise IncusError(f"transport error: {exc}") from exc
        if raw:
            if response.status_code >= 400:
                raise IncusError(f"http {response.status_code}: {response.text[:200]}")
            return response.content
        return await self._handle_envelope(response, wait=wait, wait_timeout=wait_timeout)

    async def _handle_envelope(self, response, *, wait=True, wait_timeout=60):
        # identycznie do dzisiejszej logiki, ale async await
        # dla "async" response type: await self._wait_operation(...)
        ...

    async def _wait_operation(self, operation_url, wait_timeout):
        wait_response = await self._client.get(f"{operation_url}/wait",
                                               params={"timeout": wait_timeout})
        ...
```
Lifecycle: `create_app()` tworzy klienta, `@app.teardown_appcontext` lub `atexit` woła `asyncio.run(client.close())` przy shutdownie. Alternatywnie — `app.extensions["incus"] = IncusRestClient()` i close w `atexit.register(lambda: asyncio.get_event_loop().run_until_complete(client.close()))`.

### Controllers
```python
class InstancesController:
    def __init__(self, client: IncusRestClient):
        self._client = client

    # GET /1.0/instances
    async def list_instances(self, project="default", filter=None) -> list[InstanceModel]:
        return await self._client.get("/1.0/instances",
            params={"recursion": 1, "project": project, "filter": filter})
```
Każda metoda `async def`, zwraca to samo co wcześniej (Pydantic models / `OperationModel` / `EmptySyncResponse` / `bytes`). Każda metoda poprzedzona komentarzem `# VERB /1.0/path (async|sync|raw)`.

### Blueprints — Flask 2+ async routes
```python
from flask import Blueprint, current_app, jsonify, request
from controllers.instances import InstancesController

bp = Blueprint("instances", __name__, url_prefix="/instances")

def _ctrl(): return InstancesController(current_app.extensions["incus"])

@bp.get("")
async def list_instances():
    project = request.args.get("project", "default")
    filter_ = request.args.get("filter")
    data = await _ctrl().list_instances(project=project, filter=filter_)
    return jsonify(data)

@bp.post("")
async def create_instance():
    project = request.args.get("project", "default")
    body = request.get_json(force=True)
    data = await _ctrl().create_instance(body=body, project=project)
    return jsonify(data), 202
```
Flask async wymaga `pip install flask[async]` (dociąga `asgiref`). Status codes identyczne do obecnego kodu (202, 204, raw `Response`, 501).

### Bulk / concurrent — gdzie async się opłaca
- Endpoint agregacyjny, np. `GET /instances/states` → `asyncio.gather(*[ctrl.instance_state(n) for n in names])`
- Equipment export wielu zasobów naraz (grupy, wolumeny)
- Per-request: klient wywołuje N endpointów równolegle z różnych taskó
w → każdy route obsługuje się na własnej coroutine, I/O do daemona Incusa równolegle.

### Models (bez zmian)
Pydantic z `ConfigDict(extra="allow")`, re-use: `OperationModel`, `EmptySyncResponse`, `Access`, `InstanceSnapshot`, `InstanceBackup`.

### Kolaps wariantów URL (bez zmian)
`?recursion=1/2` i `?public` to ten sam Flask route — jedna metoda kontrolera z parametrem `recursion: int = 0` / `public: bool = False` przekazywanym dalej do `params={...}`.

---

## Fazy

### Faza 0 — Migracja na async (prerekwizyt)
1. Dodać `flask[async]` do `requirements.txt`
2. Przepisać `utility/rest_client.py` na `httpx.AsyncClient` + wszystkie metody `async def`
3. Przepisać istniejące kontrolery na `async def`:
   - `controllers/instances.py`, `controllers/instances_exec.py`, `controllers/instances_files.py`
4. Przepisać istniejące blueprinty na `async def`:
   - `blueprints/instances_bp.py`, `blueprints/instancesExec_bp.py`
5. Shutdown hook dla `AsyncClient` w `app.py` (`atexit` + `asyncio.run(client.aclose())`) — lub kontekst lifespan
6. Smoke test istniejących 21 route'ów — zero regresji

### Faza 1 — Dokończenie instances (~25 endpointów, async)
- `controllers/instances_snapshots.py` — `list/create/info/update/patch/rename/delete_snapshot` (POST i DELETE async, PATCH → 204)
- `controllers/instances_backups.py` — CRUD + `export_backup` (raw bytes, `Response(mimetype="application/octet-stream")`)
- `controllers/instances_metadata.py` — `get/update/patch_metadata` + `list_templates` / `get_template` (raw) / `put_template` (post_raw) / `delete_template`
- `controllers/instances_misc.py` — `create_bitmap` (async), `debug_memory` (raw), `debug_repair`
- Blueprinty z `async def`, prefix `/instances`, unikalne `Blueprint(name)`
- Model `InstanceMetadata` dopisany do `models/instance_model.py`

### Faza 2 — Images (priorytet, 17 endpointów)
- `controllers/images.py` — `ImagesController` (async): list (z `recursion`/`public`), create (JSON) + upload (octet-stream z `X-Incus-*`), CRUD, export raw + push export async, refresh, create_image_secret, aliases CRUD + rename
- `blueprints/images_bp.py` (prefix `/images`) — **statyczne `/aliases*` przed dynamicznym `/<fingerprint>`**; dispatcher po `request.content_type` dla POST `/images`
- `models/image_model.py` — `ImageModel`, `ImageAliasModel`, `ImageSource`, `ImageMetadata`

### Faza 3 — Server / meta / warnings (10 endpointów)
- `controllers/server.py` — `root`, `server_info(public)`, `update_server`, `patch_server`, `events_stream` (**placeholder 501**), `resources`, `metrics` (raw), `metadata_configuration`
- `controllers/warnings.py` — `list_warnings(recursion)`, `warning_info`, `update_warning`, `delete_warning`
- `blueprints/server_bp.py` (prefix `""`, route `/server` → `/1.0`), `blueprints/warnings_bp.py` (`/warnings`)
- Modele: `server_model.py`, `resources_model.py`, `warning_model.py`

### Faza 4 — Profiles + Projects (11 endpointów)
- `controllers/profiles.py` (CRUD + rename), `controllers/projects.py` (CRUD + rename async + `project_access` + `project_state`)
- Blueprinty: `/profiles`, `/projects`
- Modele: `profile_model.py`, `project_model.py`

### Faza 5 — Networks core (26 endpointów)
- `controllers/networks.py` — CRUD + rename + `network_leases`, `network_state`
- `controllers/networks_forwards.py`, `controllers/networks_load_balancers.py` (+ `load_balancer_state`), `controllers/networks_peers.py`
- 4 blueprinty, prefix `/networks` (unikalne nazwy)
- `models/network_model.py` — `NetworkModel`, `NetworkState`, `NetworkLease`, `NetworkForward`, `NetworkForwardPort`, `NetworkLoadBalancer`, `NetworkLoadBalancerState`, `NetworkPeer`

### Faza 6 — Network accessories (22 endpointy)
- `controllers/network_acls.py` (+ `acl_log` raw), `controllers/network_address_sets.py`, `controllers/network_allocations.py`, `controllers/network_integrations.py`, `controllers/network_zones.py`, `controllers/network_zones_records.py`
- 6 blueprintów, modele per subdomena

### Faza 7 — Storage (~40 endpointów)
- `controllers/storage_pools.py` (+ `pool_resources`)
- `controllers/storage_volumes.py` (list z/bez `{type}`, CRUD, rename async, `volume_state`, `volume_nbd`/`volume_sftp` placeholdery, `import_volume_from_backup` octet-stream)
- `controllers/storage_volumes_snapshots.py`, `..._backups.py` (export raw), `..._bitmaps.py`, `..._files.py` (wzór `instances_files.py`)
- `controllers/storage_buckets.py`, `..._keys.py`, `..._backups.py` (export raw)
- 9 blueprintów, prefix `/storage-pools`, unikalne nazwy
- `models/storage_model.py` — komplet modeli

### Faza 8 — Cluster + Certificates + Operations (~20 endpointów)
- `controllers/cluster.py` — cluster info, update (async), certificate, groups CRUD+rename, members CRUD+rename + `request_join_token` (async) + `member_state` + `member_state_action` (async)
- `controllers/certificates.py` — CRUD (z `public`)
- `controllers/operations.py` — list (recursion), info, cancel, `wait_operation(timeout, public)`, `operation_websocket` (**placeholder 501**)
- 3 blueprinty
- Modele: `cluster_model.py`, `certificate_model.py` (OperationModel re-use)

---

## Tricky endpointy
| Przypadek | Obsługa |
|---|---|
| `POST /1.0/images` (octet-stream + `X-Incus-*`) | Blueprint po `request.content_type`: JSON → `create_image(body)`, inne → `upload_image(request.get_data(), headers)` gdzie `headers = {k:v for k,v in request.headers if k.lower().startswith("x-incus-")}`; controller → `await client.post_raw(...)` |
| Binary export (images, instance backups, volume/bucket backups, debug/memory) | `await client.get(..., raw=True)` → `bytes` → `Response(data, mimetype="application/octet-stream")` |
| `POST /1.0/instances/{name}/metadata/templates?path=` | `await client.post_raw(..., content=request.get_data())` |
| `GET /1.0/instances/{name}/metadata/templates` | Rozgałęzienie w blueprincie: `path` w query → raw bytes; bez `path` → JSON list |
| `/events`, `/operations/{id}/websocket`, `/volumes/.../nbd|/sftp`, `/instances/{name}/sftp` | **Placeholdery 501**: controller `raise NotImplementedError`, blueprint `return jsonify({"error":"..."}), 501` |
| `/1.0/metrics`, `/network-acls/{name}/log` | raw → `Response(mimetype="text/plain")` |
| `?public` warianty | Ten sam Flask route, `public` z query |
| `POST /1.0/instances/{name}/rebuild` (sync\|async) | Zawsze 202 (zgodnie z obecnym `_handle_envelope` auto-wait) |
| `GET /1.0/operations/{id}/wait` | Cienki wrapper `await wait_operation(id, timeout)` używający `client.get(...)` bezpośrednio |

---

## app.py (async) — rejestracja
```python
# app.py
import atexit, asyncio
from flask import Flask

from blueprints.instances_bp import bp as instances_bp
from blueprints.instancesExec_bp import bp as instances_exec_bp
# ... (wszystkie poniższe dodawane fazami)
from utility.rest_client import IncusRestClient

def create_app() -> Flask:
    app = Flask(__name__)
    client = IncusRestClient()
    app.extensions["incus"] = client

    app.register_blueprint(instances_bp)
    app.register_blueprint(instances_exec_bp)
    # Faza 1
    # app.register_blueprint(instances_snapshots_bp)
    # app.register_blueprint(instances_backups_bp)
    # app.register_blueprint(instances_metadata_bp)
    # app.register_blueprint(instances_misc_bp)
    # Faza 2
    # app.register_blueprint(images_bp)
    # ... i tak dalej

    atexit.register(lambda: asyncio.run(client.close()))
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
```
Każdy blueprint dzielący prefix musi mieć **unikalną nazwę** w `Blueprint("unique_name", ...)`.

---

## Konwencje nazewnicze (zamrożone)
- Plik kontrolera: `controllers/<domain>[_<subdomain>].py`, klasa `<DomainPascal>Controller`
- Metody: `list_<plural>`, `<singular>_info`, `create_<singular>`, `update_<singular>`, `patch_<singular>`, `rename_<singular>`, `delete_<singular>`; akcje specjalne → suffix (`instance_state`, `export_backup`, `acl_log`, `member_state_action`, `refresh_image`, `create_image_secret`); **wszystko `async def`**
- Każda metoda z komentarzem `# VERB /1.0/path (async|sync|raw)` nad nią
- Plik blueprintu: `blueprints/<domain>[_<subdomain>]_bp.py`, funkcje route'ów `async def` + `await _ctrl().xxx()`; nazwa Blueprint unikalna
- Plik modelu: `models/<singular>_model.py`

---

## Critical files
- `utility/rest_client.py` — **Faza 0 przepisuje na async**. Po Fazie 0 nie tykać.
- `controllers/instances.py`, `instances_files.py`, `instances_exec.py` — **Faza 0** przepisuje na `async def`. Wzorzec do powielania 1:1.
- `blueprints/instances_bp.py`, `instancesExec_bp.py` — **Faza 0** na `async def`.

---

## Verification (per fazę)
1. `python app.py` (Flask async na 127.0.0.1:5000) przy dostępnym `/var/lib/incus/unix.socket` (na Windows: WSL/Linux VM). Przy `flask[async]` jeden worker obsłuży I/O concurrently — sprawdź `curl` do 2-3 endpointów wywołanych przez `xargs -P 10` żeby potwierdzić równoległość.
2. Smoke testy per faza (przykłady):
   - Faza 0: wszystkie obecne 21 route'ów nadal działa → zero regresji (`curl http://127.0.0.1:5000/instances`, `/instances/<n>/state`, `/instances/<n>/files?path=/etc/hosts`)
   - Faza 2: `curl http://127.0.0.1:5000/images?recursion=1`, `curl -o img.tar http://127.0.0.1:5000/images/<fp>/export`, upload `curl -X POST --data-binary @img.tar -H 'Content-Type: application/octet-stream'`
   - Faza 5: `curl http://127.0.0.1:5000/networks/incusbr0/leases`
   - Faza 7: `curl http://127.0.0.1:5000/storage-pools/default/volumes?recursion=2`
   - Faza 8: `curl http://127.0.0.1:5000/operations?recursion=1`, `/cluster`
3. Porównanie z daemonem: `curl --unix-socket /var/lib/incus/unix.socket http://localhost/1.0/<path>` → zawartość `.metadata` = body z agenta
4. Test równoległości: klient Python (`asyncio.gather` + `httpx.AsyncClient`) odpala 10 wywołań `/instances/<n>/state` — powinno trwać ≈ czas jednego zapytania, nie N × ten czas

---

## Czego NIE robić
- **NIE** dodawać DTO, warstwy serwisowej, base-klas `Controller`/`Blueprint`, DI-containerów
- **NIE** włączać auth middleware — `middleware/auth.py` zostaje zakomentowany
- **NIE** owijać `IncusError` w try/except w kontrolerach/blueprintach
- **NIE** mieszać sync i async — po Fazie 0 wszystko async
- **NIE** zmieniać/renameować istniejących plików poza Fazą 0 (ta zmienia sync→async in-place)
- **NIE** implementować WebSocket/SFTP/NBD inline — placeholdery 501
- **NIE** rozbijać metod na `list_x_recursive` — jedna metoda z parametrem `recursion`
- **NIE** używać `asyncio.run()` wewnątrz route'u — Flask async ma już event loop; `atexit` close tylko na shutdownie
