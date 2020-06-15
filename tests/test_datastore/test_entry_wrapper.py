import pytest
from src.datastore.entry_wrapper import Entry
import datetime


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
        assert (datetime.datetime.now().second - actual.entered_at.second) < 1
        assert actual.duration == expected.duration
        assert actual.updated_at is None
        assert actual.updated_by is None
