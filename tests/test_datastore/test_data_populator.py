import pytest
import psycopg2
from src import DATADIR
import csv


class TestDataPopulator:
    def test_create_schema(self, data_populator):
        """tests successful schema creation"""
        good = [
            "SELECT * FROM users;",
            "SELECT * FROM entries;",
        ]
        for query in good:
            data_populator.cursor.execute(query)
        with pytest.raises(psycopg2.errors.UndefinedTable):
            data_populator.cursor.execute("""SELECT * FROM blah;""")

    def test_add_users(self, data_populator):
        """tests users can be added to database from csv file"""
        data_populator.add_users()
        with open(DATADIR.joinpath("users.csv")) as users:
            reader = csv.reader(users, delimiter=",")
            reader.__next__()  # skip header
            first = reader.__next__()
            data_populator.cursor.execute(
                """
                SELECT 
                    username, 
                    has_administrator_access, 
                    email, 
                    day_of_week 
                FROM users 
                WHERE username = %s;""",
                (first[0],),
            )
            results = data_populator.cursor.fetchone()
            for i in range(3):
                r = results[i]
                f = first[i]
                if f == "True" or f == "False":
                    assert str(r) == f
                else:
                    assert r == f

    def test_add_users_no_headers(self, data_populator):
        """make sure headers don't get added to database"""
        data_populator.cursor.execute(
            """SELECT * FROM users WHERE username='username';"""
        )
        assert data_populator.cursor.fetchone() is None
