import os

import pytest
from fastapi.testclient import TestClient

from app.main import create_application


@pytest.fixture(scope="module")
def test_app():
    os.environ["ENVIRONMENT"] = "test"
    os.environ["API_KEY"] = "dummy_key"
    app = create_application()

    with TestClient(app) as test_client:
        yield test_client
