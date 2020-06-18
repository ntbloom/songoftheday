import pytest
from src.datastore.entry_wrapper import Entry
import datetime
import psycopg2


@pytest.mark.usefixtures("data_populator")
class TestEntryWrapper:
    def test_add_entry_to_database(self, entry_wrapper, sample_entry):
        """tests being able to add an entry to the database"""
        expected: Entry = sample_entry
        entry_id = entry_wrapper.add_entry_to_database(expected)
        actual = entry_wrapper.get_entry_from_database(entry_id)
        assert actual.day == expected.day
        assert actual.username == expected.username
        assert actual.artist == expected.artist
        assert actual.song_name == expected.song_name
        assert actual.year == expected.year
        assert actual.hyperlink == expected.hyperlink
        assert datetime.datetime.now().second - actual.entered_at.second < 1
        assert actual.duration == expected.duration
        assert actual.updated_at is None
        assert actual.updated_by is None

    def test_get_entry_from_database_bad_entry_id(self, entry_wrapper):
        """tests that None is returned from bad entry_id"""
        assert entry_wrapper.get_entry_from_database(9999999) is None

    def test_update_entry(self, entry_wrapper, sample_entry):
        """tests that an entry can be edited"""
        entry: Entry = sample_entry
        entry_id = entry_wrapper.add_entry_to_database(entry)
        artist = "Prince & The Revolution"
        updated_by = "Noah"
        entry_wrapper.update_entry(updated_by, entry_id, artist=artist)

        new_entry = entry_wrapper.get_entry_from_database(entry_id)
        assert new_entry.artist == artist
        assert new_entry.song_name == entry.song_name
        assert new_entry.updated_by == updated_by
        assert datetime.datetime.now().second - new_entry.updated_at.second < 1

    def test_update_entry_is_safe_bad_column(self, entry_wrapper, sample_entry):
        """tests that only valid column names can be used"""
        entry: Entry = sample_entry
        entry_id = entry_wrapper.add_entry_to_database(entry)
        with pytest.raises(psycopg2.errors.UndefinedColumn):
            entry_wrapper.update_entry(
                "Noah", entry_id, injection="year=2000; DROP TABLE entries;"
            )

    def test_update_entry_is_safe_general_injection(self, entry_wrapper, sample_entry):
        """tests against SQL injection"""
        entry: Entry = sample_entry
        entry_id = entry_wrapper.add_entry_to_database(entry)
        entry_wrapper.update_entry("Noah", entry_id, artist="new; DROP TABLE entries;")
        assert entry_wrapper.get_entry_from_database(entry_id) is not None

    def test_update_entry_returns_none_on_bad_entry_id(self, entry_wrapper):
        """tests that None is returned when entry_id doesn't make a match"""
        assert (
            entry_wrapper.update_entry("Noah", 9999999, artist="Someone Else") is None
        )

    def test_get_all_entries_no_params(self, entry_wrapper):
        """tests that all entries are retrieved"""
        all_entries = entry_wrapper.get_all_entries()
        for i in all_entries:
            assert type(i) is Entry

    def test_get_all_entries_username_param(self, entry_wrapper):
        """tests that you can search by a username"""
        username = "Noah"
        entries_by_noah = entry_wrapper.get_all_entries(username=username)
        for entry in entries_by_noah:
            assert entry.username == username

    def test_get_all_entries_returns_none_on_bad_query(self, entry_wrapper):
        """tests that None is returned when no matches are made"""
        assert entry_wrapper.get_all_entries(username="Gollum") is None

    def test_get_all_entries_two_params(self, entry_wrapper):
        """tests that more than 1 param can be used"""
        username = "Noah"
        year = 1972
        entries_by_noah_in_1972 = entry_wrapper.get_all_entries(
            username=username, year=year
        )
        for entry in entries_by_noah_in_1972:
            assert entry.username == username
            assert entry.year == year

    def test_get_all_entries_artist_perfect_match(self, entry_wrapper, sample_entry):
        """tests that you can search song_name when not using fuzzy search"""
        entry_wrapper.add_entry_to_database(sample_entry)
        entries = entry_wrapper.get_all_entries(song_name=sample_entry.song_name)
        for entry in entries:
            assert entry.song_name == sample_entry.song_name

    def test_get_all_entries_artist_does_not_fuzzy_search(
        self, entry_wrapper, sample_entry
    ):
        """tests failure to make match on fuzzy query when fuzzy is false"""
        entry_wrapper.add_entry_to_database(sample_entry)
        new_song_name = sample_entry.song_name + " XXXXXXXX"
        entries = entry_wrapper.get_all_entries(song_name=new_song_name)
        assert entries is None

    def test_get_all_entries_artist_works_fuzzy_search(
        self, entry_wrapper, sample_entry
    ):
        """tests making match on fuzzy query when fuzzy is true"""
        entry_wrapper.add_entry_to_database(sample_entry)
        new_song_name = sample_entry.song_name + " XXXXXXXXXXXX"
        entries = entry_wrapper.get_all_entries(fuzzy=True, song_name=new_song_name)
        for i in entries:
            assert i.song_name == sample_entry.song_name
