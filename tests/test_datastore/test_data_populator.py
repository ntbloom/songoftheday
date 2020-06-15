import pytest
import psycopg2
from src import DATADIR
import csv
from datetime import date


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
        """make sure 7 users are entered but not headers"""
        data_populator.cursor.execute("""SELECT * FROM users;""")
        results = data_populator.cursor.fetchall()
        assert len(results) == 7

        data_populator.cursor.execute(
            """SELECT * FROM users WHERE username='username';"""
        )
        assert data_populator.cursor.fetchone() is None

    def test_add_songs(self, data_populator):
        """make sure a song can get added"""
        with open(DATADIR.joinpath("entries.csv")) as entries:
            reader = csv.reader(entries, delimiter=",")
            reader.__next__()  # skip header
            first = reader.__next__()
            data_populator.cursor.execute(
                """
                SELECT 
                    entry_id,
                    day,
                    username,
                    artist,
                    artist_lexemes,
                    song_name,
                    song_lexemes,
                    year,
                    hyperlink,
                    duration,
                    entered_at,
                    updated_at,
                    updated_by
                FROM entries
                WHERE song_name = %s 
            """,
                (first[3],),
            )
            results = data_populator.cursor.fetchone()
            day = results[1]
            date_split = [int(i) for i in first[0].split("-")]
            expected_date = date(date_split[2], date_split[0], date_split[1])
            assert day == expected_date

            username = results[2]
            assert username == first[1]

            artist = results[3]
            assert artist == first[2]

            song = results[5]
            assert song == first[3]

            year = results[7]
            assert year == int(first[4])

            hyperlink = results[8]
            assert hyperlink == first[5]
