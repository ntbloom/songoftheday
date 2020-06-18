import pytest
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

    def test_rollback(self, pg_connector):
        """
        Queries can be rolled back successfully
        """
        pg_connector.cursor.execute("CREATE TABLE does_not_exist (id INTEGER);")
        pg_connector.rollback()
        with pytest.raises(psycopg2.errors.UndefinedTable):
            pg_connector.cursor.execute("SELECT * from does_not_exist;")
