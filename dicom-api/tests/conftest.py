""" conftest module """

import asyncio
import pytest
from fastapi.testclient import TestClient
from containers import Container
from main import get_application


container = Container()

@pytest.fixture
def client():
    """ client fixture """

    _app = get_application(container)
    yield TestClient(_app)


@pytest.fixture(scope="session")
def event_loop(request):
    """ create an instance of the default event loop for each test case """

    loop = asyncio.get_event_loop_policy().new_event_loop()

    # container = ContainerTest()
    db = container.gateways.db()
    db.create_database()

    yield loop

    loop.close()
    db.drop_database()
