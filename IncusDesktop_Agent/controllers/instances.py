from models.emptySyncRepo_model import EmptySyncResponse
from models.instance_model import InstanceModel, InstanceState
from models.operation_model import OperationModel
from utility.rest_client import IncusRestClient
from models.access_model import Access


class InstancesController:
    def __init__(self, client: IncusRestClient):
        self._client = client

    # GET /1.0/instances
    def list_instances(self, project: str = "default", filter: str | None = None) -> list[InstanceModel]:
        return self._client.get(
            "/1.0/instances",
            params={"recursion": 1, "project": project, "filter": filter},
        )

    # POST /1.0/instances  (async)
    def create_instance(self, body: dict, project: str = "default") -> OperationModel:
        return self._client.post(
            "/1.0/instances",
            json_body=body,
            params={"project": project},
        )

    # PUT /1.0/instances  (bulk state change, async)
    def bulk_update_instances(self, body: dict, project: str = "default") -> OperationModel:
        return self._client.put(
            "/1.0/instances",
            json_body=body,
            params={"project": project},
        )

    # GET /1.0/instances/{name}
    def instance_info(self, name: str, project: str = "default") -> InstanceModel:
        return self._client.get(
            f"/1.0/instances/{name}",
            params={"recursion": 1, "project": project},
        )

    # PUT /1.0/instances/{name}  (full replace, async)
    def update_instance(self, name: str, body: dict, project: str = "default") -> OperationModel:
        return self._client.put(
            f"/1.0/instances/{name}",
            json_body=body,
            params={"project": project},
        )

    # PATCH /1.0/instances/{name}  (partial merge)
    def patch_instance(self, name: str, body: dict, project: str = "default") -> EmptySyncResponse:
        return self._client.patch(
            f"/1.0/instances/{name}",
            json_body=body,
            params={"project": project},
        )

    # POST /1.0/instances/{name}  (rename / migrate, async)
    def rename_instance(self, name: str, new_name: str, project: str = "default") -> OperationModel:
        return self._client.post(
            f"/1.0/instances/{name}",
            json_body={"name": new_name},
            params={"project": project},
        )

    # DELETE /1.0/instances/{name}  (async)
    def delete_instance(self, name: str, project: str = "default") -> OperationModel:
        return self._client.delete(
            f"/1.0/instances/{name}",
            params={"project": project},
        )

    # GET /1.0/instances/{name}/access
    def instance_access(self, name: str, project: str = "default") -> Access:
        return self._client.get(
            f"/1.0/instances/{name}/access",
            params={"project": project},
        )

    # GET /1.0/instances/{name}/state
    def instance_state(self, name: str, project: str = "default") -> InstanceState:
        return self._client.get(
            f"/1.0/instances/{name}/state",
            params={"project": project},
        )

    # PUT /1.0/instances/{name}/state  (async)
    # action: start | stop | restart | freeze | unfreeze
    def set_instance_state(
        self,
        name: str,
        action: str,
        timeout: int = 30,
        force: bool = False,
        stateful: bool = False,
        project: str = "default",
    ) -> OperationModel:
        return self._client.put(
            f"/1.0/instances/{name}/state",
            json_body={
                "action": action,
                "timeout": timeout,
                "force": force,
                "stateful": stateful,
            },
            params={"project": project},
        )

    # POST /1.0/instances/{name}/rebuild  (async)
    def rebuild_instance(self, name: str, source: dict, project: str = "default") -> OperationModel:
        return self._client.post(
            f"/1.0/instances/{name}/rebuild",
            json_body={"source": source},
            params={"project": project},
        )