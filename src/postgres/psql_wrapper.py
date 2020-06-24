from sys import argv
import subprocess
from pathlib import Path
from typing import Optional


class PsqlWrapper:
    """
    PostgresConnector class is used to interact with a postgres database running a docker/test_podman container
    """

    def __init__(self, host: str, database: str):
        self.host = host  # -h flag with psql
        self.db = database  # -d flag with psql

    def execute_query(self, query: str, no_database: Optional[bool] = False) -> bytes:
        """executes a raw SQL query, returns the results as a string"""
        # args = ()
        if no_database:
            args = [
                "psql",
                "-t",  # tuples only, returns just the value of the query
                "-h",
                self.host,
                "-U",
                "postgres",
                "-c",
                query,
            ]
        else:
            args = [
                "psql",
                "-t",  # tuples only, returns just the value of the query
                "-h",
                self.host,
                "-U",
                "postgres",
                "-d",
                self.db,
                "-c",
                query,
            ]
        command = subprocess.run(args, capture_output=True)
        command.check_returncode()
        return command.stdout

    def create_database(self) -> bytes:
        """creates a new database, drops the old one if it exists"""
        drop = f"DROP DATABASE IF EXISTS {self.db};"
        self.execute_query(drop, no_database=True)
        create = f"CREATE DATABASE {self.db}"
        return self.execute_query(create, no_database=True)


if __name__ == "__main__":
    database_name = argv[1]
    sql_script = Path(argv[2])
    p = PsqlWrapper("localhost", database_name)
    p.execute_query(argv[2])
