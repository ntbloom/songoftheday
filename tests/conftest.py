from src.podman.podman import Podman
import pytest
from src import TEST_CONTAINER, POSTGRES, POSTGRES_PORT, TEST_DATABASE
from src.postgres.postgres_connector import PostgresConnector


@pytest.fixture(scope="session", autouse=False)
def postgres_creation():
    """disposable postgres database"""
    Podman.start_container(TEST_CONTAINER, POSTGRES, POSTGRES_PORT)
    yield
    Podman.force_rm_container(TEST_CONTAINER)


@pytest.fixture(scope="function")
def pg_connector():
    """disposable PostrgresConnector object"""
    p = PostgresConnector(TEST_DATABASE)
    yield p
    p.close()
