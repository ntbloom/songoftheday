import pytest
from src import TEST_FLASK_URL
import requests


@pytest.mark.usefixtures("flask_dev_server")
class TestApp:
    def test_hello_world(self):
        """tests connection to database"""
        url = f"{TEST_FLASK_URL}/hello/"
        r = requests.get(url)
        assert r.status_code == 200
        assert r.text == "Hello, world"
