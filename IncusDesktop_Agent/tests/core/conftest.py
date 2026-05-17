import time
import pytest
import docker
import requests

from Utilities.consts import Tests


@pytest.fixture(scope="session")
def base_url():
    return Tests.DEFAULT_TESTS_URL.value


def wait_for(url, timeout=30):
    for _ in range(timeout):
        try:
            if requests.get(url).status_code < 500:
                return
        except:
            pass
        time.sleep(1)
    raise TimeoutError(f"Service not ready: {url}")
