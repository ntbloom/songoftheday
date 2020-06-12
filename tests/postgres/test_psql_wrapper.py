from src.postgres.psql_wrapper import PsqlWrapper
from src import TEST_DATABASE


class TestPsqlWrapper:
    """helper test class for testing that sample data gets propagated properly"""

    def test_execute_query(self):
        """
        psql is able to make raw sql query correctly
        """
        psql_wrapper = PsqlWrapper("localhost", TEST_DATABASE)
        query = "SELECT 1+1;"
        result = psql_wrapper.execute_query(query).strip()
        assert result == b"2"
