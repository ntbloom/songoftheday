import pytest
from src import TEST_FLASK_URL, DATADIR
import requests
import subprocess


@pytest.mark.usefixtures("flask_dev_server", "load_data_once")
class TestApp:
    """
    Test API endpoints.  Tests here largely rely on sample data not changing
    tremendously, so if tests start failing, consider that the parametrized queries may
    no longer be valid.
    """

    def test_hello_world(self):
        """tests connection to database"""
        url = f"{TEST_FLASK_URL}/hello/"
        r = requests.get(url)
        assert r.status_code == 200
        assert r.text == "Hello, world"

    def test_get_entries_no_params(self):
        """tests get_entries() method with no params"""
        url = f"{TEST_FLASK_URL}/get-entries/"
        r = requests.get(url)
        assert r.status_code == 200

        payload = r.json()
        entries_file = DATADIR.joinpath("entries.csv")
        expected_length = int(
            subprocess.check_output(
                f"wc -l {entries_file} | awk '{{ print $1 }}'", shell=True
            )
        )
        assert expected_length == len(payload) + 1

    def test_get_entries_no_results(self):
        """tests 204 response: No Content when no matches"""
        url = f"{TEST_FLASK_URL}/get-entries/?year=999999"
        r = requests.get(url)
        assert r.status_code == 204

    @pytest.mark.parametrize(
        "args,expected_song_name,expected_len,expected_status_code",
        [
            ("?year=1906", "Bella Ciao", 1, 200),
            ("?fuzzy=True&song_name=Ciao", "Bella Ciao", 1, 200),
            ("?fuzzy=False&song_name=Ciao", None, 0, 204),
            ("?song_name=Ciao", None, 0, 204),
            ("?year=1970&username=Dr. Q", "Sixty Years On", 1, 200),
        ],
    )
    def test_get_entries_with_multiple_params(
        self, args, expected_song_name, expected_len, expected_status_code
    ):
        """
        Tests get-entries/ with multiple search params. Test for expected quantity
        """
        url = f"{TEST_FLASK_URL}/get-entries/{args}"
        r = requests.get(url)

        assert r.status_code == expected_status_code
        if expected_status_code == 200:
            payload = r.json()
            assert payload[0]["song_name"] == expected_song_name
            assert len(payload) == expected_len
