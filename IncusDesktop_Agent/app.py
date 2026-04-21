# app.py
from flask import Flask

from blueprints.instances_bp import bp as instances_bp
from blueprints.instancesExec_bp import bp as instances_exec_bp
from utility.rest_client import IncusRestClient


def create_app() -> Flask:
    app = Flask(__name__)

    app.extensions["incus"] = IncusRestClient()

    app.register_blueprint(instances_bp)
    app.register_blueprint(instances_exec_bp)
    # app.register_blueprint(images_bp)
    # app.register_blueprint(networks_bp)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)