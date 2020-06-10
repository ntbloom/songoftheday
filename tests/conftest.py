from src.podman.podman import Podman
import pytest
from src import TEST_CONTAINER, POSTGRES, POSTGRES_PORT


@pytest.fixture(scope="session", autouse=False)
def postgres_creation():
    """disposable postgres database"""
    Podman.start_container(TEST_CONTAINER, POSTGRES, POSTGRES_PORT)
    yield
    Podman.stop_container(TEST_CONTAINER)
