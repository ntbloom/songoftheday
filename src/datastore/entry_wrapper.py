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
        entries = self.get_all_entries(entry_id=entry_id)
        if entries:
            return entries[0]
        return None

    def update_entry(
        self, updated_by: str, entry_id: int, **kwargs: Union[str, int, date]
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
        self, fuzzy: Optional[bool] = False, **kwargs: Union[str, int, date]
    ) -> Optional[List[Entry]]:
        """
        Returns all entries that match param args specified in **kwargs. If no params,
        return all entries. Returns None if no matches. If fuzzy, search song_lexemes
        and artist_lexemes instead of song_name and artist.
        """
        where_clause = ""
        values = []
        wheres = []
        if kwargs:
            for k, v in kwargs.items():
                if fuzzy and (k == "song_name" or k == "artist"):
                    wheres.append(
                        # fuzzy search query. Likely needs tweaking and/or a custom dict
                        f"""
                        {k} @@ to_tsquery('english', regexp_replace(%s, '\s+',' | '))
                        """
                    )
                else:
                    wheres.append(f"{quote_ident(k, self.cursor)} = %s")
                values.append(v)
            where_clause = f" WHERE {wheres[0]}"
        if len(wheres) > 1:
            for condition in wheres:
                if wheres.index(condition) > 0:
                    where_clause += f" AND {condition}"
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
