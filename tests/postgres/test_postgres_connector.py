import pytest
from src import TEST_DATABASE
from src.postgres.postgres_connector import PostgresConnector
import psycopg2


class TestPostgresConnectorClass:
    def test_connection_to_database(self, pg_connector):
        """
        Can we make a proper database connection?
        """
        pg_connector.cursor.execute("""SELECT 1+1;""")
        result = pg_connector.cursor.fetchone()[0]
        assert result == 2

    def test_commit(self, pg_connector):
        """
        No errors thrown on commit()
        """
        pg_connector.commit()

    def test_close(self, pg_connector):
        """
        Connection is properly closed and unable to run additional queries
        """
        pg_connector.close()
        with pytest.raises(psycopg2.InterfaceError):
            pg_connector.cursor.execute("""SELECT 1+1;""")

    def test_query_no_parameters(self, pg_connector):
        """
        Can we pass a simple string as a query
        """
        actual = pg_connector.query("SELECT 1+1")
        expected = [(2,)]
        assert actual == expected

    def test_query_with_params(self, pg_connector):
        """
        Can we parametize a query
        """
        actual = pg_connector.query("""SELECT 1 + %s""", (1,))
        expected = [(2,)]
        assert actual == expected
