from src.podman.podman import Podman
from src.postgres.psql_wrapper import PsqlWrapper
import pytest
from src import (
    TEST_CONTAINER,
    POSTGRES,
    POSTGRES_PORT,
    TEST_DATABASE,
    HOST,
    DATADIR,
    SCHEMA,
    PYTHON,
    APP,
    TEST_FLASK_URL,
    COMMON_PASSWORDS,
    TEST_JWT_KEY,
)
from src.postgres.postgres_connector import PostgresConnector
from src.datastore.data_populator import DataPopulator
from src.datastore.entry_wrapper import EntryWrapper, Entry
from src.postgres.password_manager import PasswordManager
from src.datastore.jwt_manager import JWTManager
from datetime import date
import requests
import subprocess
import os


@pytest.fixture(scope="session", autouse=False)
def postgres_creation():
    """disposable postgres database"""
    Podman.start_container(TEST_CONTAINER, POSTGRES, POSTGRES_PORT)
    yield
    Podman.force_rm_container(TEST_CONTAINER)


@pytest.fixture()
def pg_connector():
    """disposable PostrgresConnector object"""
    p = PostgresConnector(TEST_DATABASE)
    yield p
    p.close()


@pytest.fixture()
def data_populator():
    """automatically populate data in the database"""
    psql = PsqlWrapper(HOST, TEST_DATABASE)  # initialize the database
    psql.create_database()
    dp = DataPopulator(
        TEST_DATABASE,
        HOST,
        SCHEMA,
        DATADIR.joinpath("users.csv"),
        DATADIR.joinpath("entries.csv"),
    )
    yield dp
    dp.close()


@pytest.fixture(scope="session")
def load_data_once():
    """populate data in the database once per class"""
    psql = PsqlWrapper(HOST, TEST_DATABASE)
    psql.create_database()
    dp = DataPopulator(
        TEST_DATABASE,
        HOST,
        SCHEMA,
        DATADIR.joinpath("users.csv"),
        DATADIR.joinpath("entries.csv"),
    )
    dp.close()


@pytest.fixture()
def entry_wrapper():
    """disposable EntryWrapper object"""
    entry_wrapper = EntryWrapper(TEST_DATABASE, HOST)
    yield entry_wrapper
    entry_wrapper.close()


@pytest.fixture()
def sample_entry():
    """disposable Entry object"""
    day = date(1999, 12, 31)
    username = "N Bomb"
    artist = "Prince"
    song_name = "1999"
    year = 1982
    hyperlink = "https://www.youtube.com/watch?v=rblt2EtFfC4"
    entry = Entry(day, username, artist, song_name, year, hyperlink)
    yield entry


@pytest.fixture(scope="class")
def flask_dev_server():
    """starts a flask development server, shuts it down after tests"""
    os.environ["FLASK_ENV"] = "testing"
    server = subprocess.Popen([PYTHON, APP], stdout=subprocess.DEVNULL)
    pid = server.pid

    # wait for server to load before yielding
    loading = True
    while loading:
        try:
            assert requests.get(f"{TEST_FLASK_URL}/hello/").status_code == 200
            loading = False
        except requests.exceptions.ConnectionError:
            pass
    yield
    kill = subprocess.run(["kill", "-9", str(pid)])
    kill.check_returncode()


@pytest.fixture()
def password_manager():
    """disposable password manager object"""
    pw_mgr = PasswordManager(TEST_DATABASE, HOST)
    yield pw_mgr
    pw_mgr.close()


@pytest.fixture()
def add_common_passwords(data_populator):
    """adds txt file of common passwords to database"""
    psql = PsqlWrapper(HOST, TEST_DATABASE)
    query = (
        "\COPY common_passwords (password) FROM '"
        + str(COMMON_PASSWORDS)
        + "' (FORMAT csv);"
    )
    psql.execute_query(query)


@pytest.fixture()
def jwt_manager():
    jwt = JWTManager(TEST_JWT_KEY)
    return jwt
