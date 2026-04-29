# app.py
import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv

import atexit

from flask import Flask, jsonify

from Agent.blueprints.instances_bp import bp as instances_bp
from Agent.blueprints.instancesExec_bp import bp as instances_exec_bp
from Agent.blueprints.instances_snapshots_bp import bp as instances_snapshots_bp
from Agent.blueprints.instances_backups_bp import bp as instances_backups_bp
from Agent.blueprints.instances_metadata_bp import bp as instances_metadata_bp
from Agent.blueprints.instances_misc_bp import bp as instances_misc_bp
from Agent.blueprints.images_bp import bp as images_bp
from Agent.blueprints.server_bp import bp as server_bp
from Agent.blueprints.warnings_bp import bp as warnings_bp
from Agent.blueprints.profiles_bp import bp as profiles_bp
from Agent.blueprints.projects_bp import bp as projects_bp
from Agent.blueprints.networks_bp import bp as networks_bp
from Agent.blueprints.networks_forwards_bp import bp as networks_forwards_bp
from Agent.blueprints.networks_load_balancers_bp import bp as networks_load_balancers_bp
from Agent.blueprints.networks_peers_bp import bp as networks_peers_bp
from Agent.blueprints.network_acls_bp import bp as network_acls_bp
from Agent.blueprints.network_address_sets_bp import bp as network_address_sets_bp
from Agent.blueprints.network_allocations_bp import bp as network_allocations_bp
from Agent.blueprints.network_integrations_bp import bp as network_integrations_bp
from Agent.blueprints.network_zones_bp import bp as network_zones_bp
from Agent.blueprints.network_zones_records_bp import bp as network_zones_records_bp
from Agent.blueprints.storage_pools_bp import bp as storage_pools_bp
from Agent.blueprints.storage_volumes_bp import bp as storage_volumes_bp
from Agent.blueprints.storage_volumes_snapshots_bp import bp as storage_volumes_snapshots_bp
from Agent.blueprints.storage_volumes_backups_bp import bp as storage_volumes_backups_bp
from Agent.blueprints.storage_volumes_bitmaps_bp import bp as storage_volumes_bitmaps_bp
from Agent.blueprints.storage_volumes_files_bp import bp as storage_volumes_files_bp
from Agent.blueprints.storage_buckets_bp import bp as storage_buckets_bp
from Agent.blueprints.storage_buckets_keys_bp import bp as storage_buckets_keys_bp
from Agent.blueprints.storage_buckets_backups_bp import bp as storage_buckets_backups_bp
from Agent.blueprints.cluster_bp import bp as cluster_bp
from Agent.blueprints.certificates_bp import bp as certificates_bp
from Agent.blueprints.operations_bp import bp as operations_bp

from Agent.blueprints.scenarios.instance_bp import bp as scenarios_instance_bp
from Agent.blueprints.scenarios.host_bp import bp as scenarios_host_bp
from Agent.blueprints.scenarios.dashboard_bp import bp as scenarios_dashboard_bp
from Agent.blueprints.scenarios.runs_bp import bp as scenarios_runs_bp

from Agent.blueprints.rawCommands.examples_bp import bp as raw_examples_bp

from Agent.utility.rest_client import IncusRestClient


def create_app() -> Flask:
    load_dotenv()
    app = Flask(__name__)

    client = IncusRestClient()

    @app.before_request
    def check_requirements():
        is_dev =os.getenv("DEVELOPER_MODE")

        if not Path(IncusRestClient.DEFAULT_SOCKET).exists() and not is_dev:
            return jsonify({"Error": "Incus is not installed and default unix socket file was not found. Install incus then run api again."}), 503
        return None

    app.extensions["incus"] = client

    app.register_blueprint(instances_bp)
    app.register_blueprint(instances_exec_bp)
    app.register_blueprint(instances_snapshots_bp)
    app.register_blueprint(instances_backups_bp)
    app.register_blueprint(instances_metadata_bp)
    app.register_blueprint(instances_misc_bp)
    app.register_blueprint(images_bp)
    app.register_blueprint(server_bp)
    app.register_blueprint(warnings_bp)
    app.register_blueprint(profiles_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(networks_bp)
    app.register_blueprint(networks_forwards_bp)
    app.register_blueprint(networks_load_balancers_bp)
    app.register_blueprint(networks_peers_bp)
    app.register_blueprint(network_acls_bp)
    app.register_blueprint(network_address_sets_bp)
    app.register_blueprint(network_allocations_bp)
    app.register_blueprint(network_integrations_bp)
    app.register_blueprint(network_zones_bp)
    app.register_blueprint(network_zones_records_bp)
    app.register_blueprint(storage_pools_bp)
    app.register_blueprint(storage_volumes_bp)
    app.register_blueprint(storage_volumes_snapshots_bp)
    app.register_blueprint(storage_volumes_backups_bp)
    app.register_blueprint(storage_volumes_bitmaps_bp)
    app.register_blueprint(storage_volumes_files_bp)
    app.register_blueprint(storage_buckets_bp)
    app.register_blueprint(storage_buckets_keys_bp)
    app.register_blueprint(storage_buckets_backups_bp)
    app.register_blueprint(cluster_bp)
    app.register_blueprint(certificates_bp)
    app.register_blueprint(operations_bp)

    # Scenarios (agent-side orchestrations)
    app.register_blueprint(scenarios_instance_bp)
    app.register_blueprint(scenarios_host_bp)
    app.register_blueprint(scenarios_dashboard_bp)
    app.register_blueprint(scenarios_runs_bp)

    # rawCommands (host shell-out)
    app.register_blueprint(raw_examples_bp)

    atexit.register(lambda: asyncio.run(client.close()))

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
