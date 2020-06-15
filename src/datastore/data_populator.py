from src.postgres.postgres_connector import PostgresConnector
from pathlib import Path
import psycopg2


class DataPopulator(PostgresConnector):
    def __init__(self, database: str, host: str):
        """
        Static class that adds data to the Postgres database according to the schema
        """
        super().__init__(database, host)

    def create_schema(self, file: Path) -> None:
        """
        Populates a database with a schema on a particular host
        """
        with open(file, "r") as schema:
            sql = schema.read().split(";")
            for i in sql:
                try:
                    self.cursor.execute(i)
                except psycopg2.ProgrammingError:
                    pass
