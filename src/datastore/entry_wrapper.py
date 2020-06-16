from typing import NamedTuple, Optional, Union, Dict, List
from datetime import date
from src.postgres.postgres_connector import PostgresConnector
from psycopg2.extensions import quote_ident


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
        self.commit()
        return entry_id

    def get_entry_from_database(self, entry_id: int) -> Optional[Entry]:
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
        if resp is None:
            return None
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
            updated_by=resp[10],
        )
        return entry

    def update_entry(
        self, updated_by: str, entry_id: int, **kwargs: Dict[str, Union[str, int, date]]
    ) -> Optional[Entry]:
        """
        Edits a given entry according to params named in kwargs
        """
        for k, v in kwargs.items():
            self.cursor.execute(
                f"""
                UPDATE entries
                SET 
                    {quote_ident(k,self.cursor)} = %s,
                    updated_at = now(), 
                    updated_by = %s
                WHERE entry_id = %s;
            """,
                (v, updated_by, entry_id),
            )
            self.commit()
        return self.get_entry_from_database(entry_id)

    def get_all_entries(
        self, **kwargs: Dict[str, Union[str, int, date]]
    ) -> Optional[List[Entry]]:
        """
        Returns all entries that match param args specified in **kwargs. If no params,
        return all entries. Returns None if no matches.
        """
        where_clause = ""
        values = []
        if kwargs:
            item = kwargs.popitem()
            values.append(item[1])
            where_clause = f"WHERE {quote_ident(item[0], self.cursor)} = %s"
            while len(kwargs) != 0:
                item = kwargs.popitem()
                values.append(item[1])
                where_clause += f" AND {quote_ident(item[0], self.cursor)} = %s"
        params = tuple(values)
        self.cursor.execute(
            f"""
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
            {where_clause}
            """,
            params,
        )
        resp = self.cursor.fetchall()
        if len(resp) == 0:
            return None
        else:
            entries = []
            for i in resp:
                entry = Entry(
                    entry_id=i[0],
                    day=i[1],
                    username=i[2],
                    artist=i[3],
                    song_name=i[4],
                    year=i[5],
                    hyperlink=i[6],
                    duration=i[7],
                    entered_at=i[8],
                    updated_at=i[9],
                    updated_by=i[10],
                )
                entries.append(entry)
        return entries
