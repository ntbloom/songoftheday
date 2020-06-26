import pytest
from freezegun import freeze_time
from time import time, gmtime
from src import TEST_JWT_KEY, JWT_DAYS_VALID, TEST_JWT_ALGO
from src.datastore.jwt_manager import JWTManager, JWTError, Token
from hypothesis import given
import hypothesis.strategies as st
import json
import jwt


class TestJWTManager:
    def test_jwt_token(self, jwt_manager):
        """
        Tests that a token can be automatically created. Time is checked within a margin
        of 2 seconds
        """
        username = "Name"
        level = 1
        algorithm = TEST_JWT_ALGO
        raw = Token(username, level, algorithm)

        assert raw.usr == username
        assert raw.lev == level
        assert raw.alg == algorithm
        now = time()
        assert raw.iat - now < 2
        expires = gmtime(raw.exp)[7]
        today = gmtime(now)[7]

        # TODO: fix so this test will pass on or near Dec 31
        assert expires - today == JWT_DAYS_VALID

    @given(name=st.text())
    def test_encrypt_and_decrypt(self, jwt_manager, name):
        """
        Property-based test on encrypt/decrypt
        """
        token = Token(name, 1, TEST_JWT_ALGO)
        encrypted = jwt_manager.encrypt(token)
        decrypted = jwt_manager.decrypt(encrypted)
        assert decrypted == token

    def test_decrypt_raises_jwterror_with_bad_key(self, jwt_manager):
        """
        Expected JWTError when given bad encrypted token
        """
        invalid = b"tZSI6IiIsImxldmVsIjoxLCJpYXQiOjE1OTMxODAyMDMuODMzMDk4MiwiZXhwIjoxNTkzMjY2NjAzLjgzMzA5ODJ9.wU4I-Na4HZeJJaA3LCGCNLTBa7wdXTtreC246MONdj_dT5F4sdJ2p-F4lJaWysHC6_TeXm7JybNbbyyaGHW7pw"
        with pytest.raises(JWTError):
            jwt_manager.decrypt(invalid)

    # def test_decrypt_raises_jwterror_with
