from typing import NamedTuple, Optional, Union, Dict
from datetime import date
from src.postgres.postgres_connector import PostgresConnector


class Entry(NamedTuple):
    day: date
    username: str
    artist: str
    song_name: str
    year: int
    hyperlink: str
    entered_at: Optional[date] = None
    entry_id: Optional[int] = None
    duration: Optional[int] = None  # in seconds
    updated_at: Optional[date] = None
    updated_by: Optional[str] = None


class EntryWrapper(PostgresConnector):
    def __init__(self, database: str, host: Optional[str] = "localhost"):
        """
        Manages making entries to the database.
        """
        super().__init__(database, host)

    def add_entry_to_database(self, entry: Entry) -> int:
        """
        Adds an entry to the database, returns the entry_id
        """
        self.cursor.execute(
            """
            INSERT INTO entries (
                day,
                username,
                artist,
                song_name,
                year,
                hyperlink,
                duration 
            ) VALUES (%s,%s, %s, %s, %s, %s, %s)
            RETURNING entry_id;
        """,
            (
                entry.day,
                entry.username,
                entry.artist,
                entry.song_name,
                entry.year,
                entry.hyperlink,
                entry.duration,
            ),
        )
        entry_id = self.cursor.fetchone()[0]
        return entry_id

    def get_entry_from_database(self, entry_id: int) -> Entry:
        """
        Gets an entry from the database from an entry_id as an Entry object
        """
        self.cursor.execute(
            """
            SELECT
                entry_id,
                day,
                username,
                artist,
                song_name,
                year,
                hyperlink,
                duration,
                entered_at,
                updated_at,
                updated_by
            FROM entries
            WHERE entry_id = %s
        """,
            (entry_id,),
        )
        resp = self.cursor.fetchone()
        entry = Entry(
            entry_id=resp[0],
            day=resp[1],
            username=resp[2],
            artist=resp[3],
            song_name=resp[4],
            year=resp[5],
            hyperlink=resp[6],
            duration=resp[7],
            entered_at=resp[8],
            updated_at=resp[9],
        )
        return entry

    def update_entry(
        self, updated_by: str, entry_id: int, **kwargs: Dict[str, Union[str, int, date]]
    ) -> Entry:
        """
        Edits a given entry according to params named in kwargs
        """
        pass
