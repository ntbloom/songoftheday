import pytest
from src import TEST_FLASK_URL, DATADIR
import requests
import subprocess


@pytest.mark.usefixtures("flask_dev_server", "load_data_once")
class TestApp:
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

    def test_get_entries_with_single_param_year(self):
        """tests get_entries() with year search params"""
        url = f"{TEST_FLASK_URL}/get-entries/?year=1906"
        r = requests.get(url)
        assert r.status_code == 200

        payload = r.json()
        assert payload[0]["song_name"] == "Bella Ciao"
