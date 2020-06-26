from pathlib import Path
from os.path import abspath

"""
This file contains various global variables used as configs, mostly for testing.
"""

# file directories
HOMEDIR: Path = Path(__file__).parent.parent
SOURCEDIR: Path = HOMEDIR.joinpath("src")
TESTDIR: Path = HOMEDIR.joinpath("tests")
DATADIR: Path = TESTDIR.joinpath("utils").joinpath("test_data")

# testing variables
TEST_CONTAINER: str = "pg-test"
TEST_DATABASE: str = "sotd_test"
TEST_FLASK_PORT: int = 5000
FLASK_API_VERSION: str = "1.0"
TEST_FLASK_URL: str = f"http://127.0.0.1:{str(TEST_FLASK_PORT)}/v{FLASK_API_VERSION}"
TEST_JWT_KEY: str = "this_is_a_bad_key"
TEST_JWT_ALGO: str = "HS512"

# Python environment variables for running Flask dev server from subprocess module
APP = abspath(HOMEDIR.joinpath("app.py"))
PYTHON = abspath(HOMEDIR.joinpath("venv").joinpath("bin").joinpath("python"))

# container images
POSTGRES: str = "docker.io/library/postgres"
POSTGRES_PORT: int = 5432
HOST: str = "localhost"

# database files
SCHEMA: Path = SOURCEDIR.joinpath("postgres").joinpath(Path("schema.sql"))

# authentication variables
SALT_LENGTH: int = 8
MIN_PW_LENGTH: int = 10
COMMON_PASSWORDS: Path = SOURCEDIR.joinpath("postgres").joinpath("common_passwords.txt")
JWT_DAYS_VALID: int = 1
