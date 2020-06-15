from src.postgres.postgres_connector import PostgresConnector
from pathlib import Path
import psycopg2
import csv


class DataPopulator(PostgresConnector):
    def __init__(
        self, database: str, host: str, schema: Path, users: Path, entries: Path
    ):
        """
        Static class that adds data to the Postgres database according to the schema
        """
        super().__init__(database, host)
        self.schema = schema
        self.users = users
        self.entries = entries
        self._create_schema()

    def _create_schema(self) -> None:
        """
        Populates a database with a schema on a particular host
        """
        with open(self.schema, "r") as schema:
            sql = schema.read().split(";")
            for i in sql:
                try:
                    self.cursor.execute(i)
                except psycopg2.ProgrammingError:
                    pass

    def add_users(self) -> None:
        """adds the users to the database"""
        with open(self.users) as users:
            reader = csv.reader(users, delimiter=",")
            reader.__next__()
            for line in reader:
                self.cursor.execute(
                    """
                    INSERT INTO users (
                        username, 
                        has_administrator_access, 
                        email, 
                        day_of_week
                    ) VALUES (%s, %s, %s, %s)
                """,
                    (line[0], line[1], line[2], line[3]),
                )
