import pytest
from src import TEST_FLASK_URL, DATADIR
import requests
import subprocess
from os.path import abspath


@pytest.mark.usefixtures("flask_dev_server", "load_data_once")
class TestApp:
    def test_hello_world(self):
        """tests connection to database"""
        url = f"{TEST_FLASK_URL}/hello/"
        r = requests.get(url)
        assert r.status_code == 200
        assert r.text == "Hello, world"

    def test_get_all_entries(self):
        """tests get_all_entries() method"""
        url = f"{TEST_FLASK_URL}/get-all-entries/"
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
