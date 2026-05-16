import pytest
import docker

@pytest.fixture(scope="session", autouse=True)
def setup():
    client = docker.from_env()
    c = client.containers.run(
        "IncusDesktopTests:latest"
    )