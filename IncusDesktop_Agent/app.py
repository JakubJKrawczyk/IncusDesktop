# app.py
import asyncio
import atexit

from flask import Flask

from blueprints.instances_bp import bp as instances_bp
from blueprints.instancesExec_bp import bp as instances_exec_bp
from blueprints.instances_snapshots_bp import bp as instances_snapshots_bp
from blueprints.instances_backups_bp import bp as instances_backups_bp
from blueprints.instances_metadata_bp import bp as instances_metadata_bp
from blueprints.instances_misc_bp import bp as instances_misc_bp
from blueprints.images_bp import bp as images_bp
from blueprints.server_bp import bp as server_bp
from blueprints.warnings_bp import bp as warnings_bp
from blueprints.profiles_bp import bp as profiles_bp
from blueprints.projects_bp import bp as projects_bp
from blueprints.networks_bp import bp as networks_bp
from blueprints.networks_forwards_bp import bp as networks_forwards_bp
from blueprints.networks_load_balancers_bp import bp as networks_load_balancers_bp
from blueprints.networks_peers_bp import bp as networks_peers_bp
from blueprints.network_acls_bp import bp as network_acls_bp
from blueprints.network_address_sets_bp import bp as network_address_sets_bp
from blueprints.network_allocations_bp import bp as network_allocations_bp
from blueprints.network_integrations_bp import bp as network_integrations_bp
from blueprints.network_zones_bp import bp as network_zones_bp
from blueprints.network_zones_records_bp import bp as network_zones_records_bp
from blueprints.storage_pools_bp import bp as storage_pools_bp
from blueprints.storage_volumes_bp import bp as storage_volumes_bp
from blueprints.storage_volumes_snapshots_bp import bp as storage_volumes_snapshots_bp
from blueprints.storage_volumes_backups_bp import bp as storage_volumes_backups_bp
from blueprints.storage_volumes_bitmaps_bp import bp as storage_volumes_bitmaps_bp
from blueprints.storage_volumes_files_bp import bp as storage_volumes_files_bp
from blueprints.storage_buckets_bp import bp as storage_buckets_bp
from blueprints.storage_buckets_keys_bp import bp as storage_buckets_keys_bp
from blueprints.storage_buckets_backups_bp import bp as storage_buckets_backups_bp
from blueprints.cluster_bp import bp as cluster_bp
from blueprints.certificates_bp import bp as certificates_bp
from blueprints.operations_bp import bp as operations_bp
from utility.rest_client import IncusRestClient


def create_app() -> Flask:
    app = Flask(__name__)

    client = IncusRestClient()
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

    atexit.register(lambda: asyncio.run(client.close()))

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
