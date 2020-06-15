from pathlib import Path

# file directories
HOMEDIR = Path(__file__).parent.parent
SOURCEDIR = HOMEDIR.joinpath("src")
TESTDIR = HOMEDIR.joinpath("test")
TESTDATADIR = TESTDIR.joinpath("test_data")

# testing variables
TEST_CONTAINER = "pg-test"
TEST_DATABASE = "sotd_test"

# container images
POSTGRES = "docker.io/library/postgres"
POSTGRES_PORT = 5432
HOST = "localhost"

# database files
SCHEMA = SOURCEDIR.joinpath("postgres").joinpath(Path("schema.sql"))
