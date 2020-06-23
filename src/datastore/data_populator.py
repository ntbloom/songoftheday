from src.postgres.postgres_connector import PostgresConnector
from pathlib import Path
import psycopg2
import csv
from src import HOST, TEST_DATABASE, SCHEMA, DATADIR, SALT_LENGTH
from secrets import token_urlsafe
from src.postgres.password_manager import PasswordManager


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
        self._add_users()
        self._add_entries()

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

    def _add_users(self) -> None:
        """
        Adds the users to the database
        """
        with open(self.users) as users:
            reader = csv.reader(users, delimiter=",")
            reader.__next__()
            for line in reader:
                salt = token_urlsafe(SALT_LENGTH)
                encrypted_pw = PasswordManager.hash(line[4], salt)
                self.cursor.execute(
                    """
                    INSERT INTO users (
                        username, 
                        has_administrator_access, 
                        email, 
                        day_of_week,
                        password, 
                        salt
                    ) VALUES (%s, %s, %s, %s, %s, %s)
                """,
                    (line[0], line[1], line[2], line[3], encrypted_pw, salt),
                )
                self.commit()

    def _add_entries(self) -> None:
        """
        Adds entries to the database
        """
        with open(self.entries) as entries:
            reader = csv.reader(entries, delimiter=",")
            reader.__next__()
            for line in reader:
                self.cursor.execute(
                    """
                    INSERT INTO entries (
                         day,
                         username,
                         artist,
                         song_name,
                         year,
                         hyperlink
                     ) VALUES (%s,%s,%s,%s,%s,%s)
                """,
                    (line[0], line[1], line[2], line[3], line[4], line[5]),
                )
                self.commit()


if __name__ == "__main__":
    dp = DataPopulator(
        TEST_DATABASE,
        HOST,
        SCHEMA,
        DATADIR.joinpath("users.csv"),
        DATADIR.joinpath("entries.csv"),
    )
