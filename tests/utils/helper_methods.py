from src.postgres.postgres_connector import PostgresConnector
from src import TEST_DATABASE, HOST
from psycopg2.extensions import quote_ident
from src import DATADIR
import csv


def get_username_data(username: str, column: str) -> str:
    """gets value from database for a given username"""
    with PostgresConnector(TEST_DATABASE, HOST) as pg:
        pg.cursor.execute(
            f"""
            SELECT {quote_ident(column,pg.cursor)} 
            FROM users
            WHERE username = %s
        """,
            (username,),
        )
        value = pg.cursor.fetchone()[0]
        return value


def get_plaintext_password(username: str) -> str:
    """retrieves plaintext password from the sample data"""
    with open(DATADIR.joinpath("users.csv")) as users:
        reader = csv.reader(users, delimiter=",")
        for line in reader:
            if line[0] == username:
                return line[4]
