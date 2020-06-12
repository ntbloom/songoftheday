import psycopg2
from psycopg2 import extensions
from typing import Optional, List, Any, Tuple


class PostgresConnector:
    """
    Wrapper class for connecting to the postgresql database
    """

    def __init__(self, database: str, host: Optional[str] = "localhost"):
        self.conn: extensions.connection = psycopg2.connect(
            dbname=database, user="postgres", host=host
        )
        self.cursor: extensions.cursor = self.conn.cursor()

    def commit(self):
        """
        Commits a query to the database
        """
        self.conn.commit()

    def close(self):
        """
        Closes connection with the database
        """
        self.conn.close()

    def query(
        self, query: str, params: Tuple[Any, ...] = None
    ) -> List[Tuple[Any, ...]]:
        """
        Write a query on the database.  Either send a raw string or a tuple for
        parametized values.
        """
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
