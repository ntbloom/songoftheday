import pytest
from freezegun import freeze_time
from time import time, localtime
import datetime
from src import TEST_JWT_KEY, JWT_DAYS_VALID, TEST_JWT_ALGO
from src.datastore.jwt_manager import JWTManager, JWTError, Token
from hypothesis import given
import hypothesis.strategies as st
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
        raw = Token(username, level)

        assert raw.usr == username
        assert raw.lev == level
        now = time()
        assert raw.iat - now < 2
        expires = localtime(raw.exp)[7]
        today = localtime(now)[7]

        # TODO: fix so this test will pass on or near Dec 31
        assert expires - today == JWT_DAYS_VALID

    @given(name=st.text())
    def test_encrypt_and_decrypt(self, jwt_manager, name):
        """
        Property-based test on encrypt/decrypt
        """
        token = Token(name, 1)
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

    def test_decrypt_raises_jwterror_with_wrong_algorithm(self):
        """
        Decoding jwt should raise exception if wrong algorithm was used
        """
        alg1 = "HS256"
        token = Token("Name", 1)
        jwt1 = JWTManager(TEST_JWT_KEY, alg1)
        bad_token = jwt1.encrypt(token)

        alg2 = "HS512"
        jwt2 = JWTManager(TEST_JWT_KEY, alg2)
        with pytest.raises(JWTError):
            jwt2.decrypt(bad_token)

    def test_decrypt_raises_jwt_error_with_wrong_key(self):
        """
        Throw JWTError when wrong encryption key is given
        """
        token = Token("Name", 1)
        bad_key = "this is a bad key"
        jwt1 = JWTManager(bad_key)
        bad_token = jwt1.encrypt(token)

        jwt2 = JWTManager(TEST_JWT_KEY)
        with pytest.raises(JWTError):
            jwt2.decrypt(bad_token)

    @pytest.mark.parametrize(
        "payload",
        [
            {"usr": "blah", "lev": 1, "iat": 123.4, "exp": 456.7, "oops": "extra"},
            {"usr": "blah", "lev": 1, "iat": 123.4},
        ],
    )
    def test_decrypt_raises_jwt_error_when_form_doesnt_match(
        self, jwt_manager, payload
    ):
        """
        Throws JWTError if token has more or fewer attributes
        """
        a = 1
        bad_token = jwt.encode(payload, TEST_JWT_KEY, TEST_JWT_ALGO)
        with pytest.raises(JWTError):
            jwt_manager.decrypt(payload)

    def test_validate_passes_happy_path(self, jwt_manager):
        """
        A valid jwt passes immediately after its creation
        """
        token = Token("Name", 1)
        encrypted = jwt_manager.encrypt(token)

        decrypted = jwt_manager.validate(encrypted)
        assert decrypted == token

    def test_validate_fails_iat_in_the_future(self, jwt_manager):
        """
        Fail jwt validation for an iat in the future
        """
        future = time() + 300
        token = Token("Name", 1, iat=future)
        encrypted = jwt_manager.encrypt(token)

        with pytest.raises(JWTError):
            jwt_manager.validate(encrypted)

    @pytest.mark.skip("fighting freezegun; look for other options")
    def test_validate_fails_if_expired(self, jwt_manager):
        """
        Fail jwt validation for an expired exp field
        """
        token = Token("Name", 1)
        encrypted = jwt_manager.encrypt(token)

        # without freeze time
        decrypted = jwt_manager.validate(encrypted)

        # with freeze time
        future = datetime.datetime.now() + datetime.timedelta(days=JWT_DAYS_VALID + 1)
        with freeze_time(future):
            exp = localtime(token.exp)
            now = localtime(time())
            with pytest.raises(JWTError):
                decrypted = jwt_manager.validate(encrypted)
