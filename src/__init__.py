from pathlib import Path

# file directories
HOMEDIR: Path = Path(__file__).parent.parent
SOURCEDIR: Path = HOMEDIR.joinpath("src")
TESTDIR: Path = HOMEDIR.joinpath("tests")
DATADIR: Path = TESTDIR.joinpath("utils").joinpath("test_data")

# testing variables
TEST_CONTAINER: str = "pg-test"
TEST_DATABASE: str = "sotd_test"

# container images
POSTGRES: str = "docker.io/library/postgres"
POSTGRES_PORT: int = 5432
HOST: str = "localhost"

# database files
SCHEMA: Path = SOURCEDIR.joinpath("postgres").joinpath(Path("schema.sql"))
