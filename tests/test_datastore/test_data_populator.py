import pytest
from src import SCHEMA
import psycopg2


class TestDataPopulator:
    def test_create_schema(self, data_populator):
        """tests successful schema creation"""
        data_populator.create_schema(SCHEMA)
        good = [
            "SELECT * FROM users;",
            "SELECT * FROM entries;",
        ]
        for query in good:
            data_populator.cursor.execute(query)
        with pytest.raises(psycopg2.errors.UndefinedTable):
            data_populator.cursor.execute("""SELECT * FROM blah;""")
