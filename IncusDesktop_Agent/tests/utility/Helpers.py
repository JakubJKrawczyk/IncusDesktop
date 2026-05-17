import requests

from Utilities import consts
from tests.utility.Exceptions import IncusTestsError


class TestsHelper:

    @staticmethod
    def check_test_instance_connection():

        response = requests.get(f"{consts.Tests.DEFAULT_TESTS_URL}")

        if response.status_code != 200:
            raise IncusTestsError("Instance for testing is down. Response status code is not 200. Check it !")
