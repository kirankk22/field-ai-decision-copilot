import pytest

from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """
    Create a FastAPI test client.

    The application is exercised in-process,
    so the test suite does not require Uvicorn
    to be running separately.
    """

    with TestClient(app) as test_client:
        yield test_client