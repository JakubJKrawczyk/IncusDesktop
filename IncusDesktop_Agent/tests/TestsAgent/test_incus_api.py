
import pytest
from Agent.controllers.incus.instances import *

#Setup section
@pytest.fixture(scope="session", autouse=True)
def one_time_setup():
   pass

@pytest.fixture(scope="session")
def controller():
    c = InstancesController()
    yield c



#Tests section
@pytest.mark.incus_api
def test_create_instance(controller):
    controller.create_instance()