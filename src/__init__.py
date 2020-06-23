from pathlib import Path
from os.path import abspath

# file directories
HOMEDIR: Path = Path(__file__).parent.parent
SOURCEDIR: Path = HOMEDIR.joinpath("src")
TESTDIR: Path = HOMEDIR.joinpath("tests")
DATADIR: Path = TESTDIR.joinpath("utils").joinpath("test_data")

# testing variables
TEST_CONTAINER: str = "pg-test"
TEST_DATABASE: str = "sotd_test"
TEST_FLASK_PORT: int = 5000
TEST_FLASK_URL: str = f"http://127.0.0.1:{str(TEST_FLASK_PORT)}"

# Python environment variables for running Flask dev server from subprocess module
APP = abspath(HOMEDIR.joinpath("app.py"))
PYTHON = abspath(HOMEDIR.joinpath("venv").joinpath("bin").joinpath("python"))

# container images
POSTGRES: str = "docker.io/library/postgres"
POSTGRES_PORT: int = 5432
HOST: str = "localhost"

# database files
SCHEMA: Path = SOURCEDIR.joinpath("postgres").joinpath(Path("schema.sql"))
