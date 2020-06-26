import pytest
from freezegun import freeze_time
from time import time, gmtime
from src import TEST_JWT_KEY, JWT_DAYS_VALID
from src.datastore.jwt_manager import JWTManager, JWTError, Token


class TestJWTManager:
    def test_jwt_token(self, jwt_manager):
        """
        Tests that a token can be automatically created. Time is checked within a margin
        of 2 seconds
        """
        username = "Name"
        level = 1
        raw = Token(username, level)

        assert raw.username == username
        assert raw.level == level
        now = time()
        assert raw.iat - now < 2
        expires = gmtime(raw.exp)[7]
        today = gmtime(now)[7]

        # TODO: fix so this test will pass on or near Dec 31
        assert expires - today == JWT_DAYS_VALID

    def test_encrypt_and_decrypt(self, jwt_manager):
        token = Token("Name", 1)
        encrypted = jwt_manager.encrypt(token)
        decrypted = jwt_manager.decrypt(encrypted)
        assert decrypted == token
