import pytest
from tests.utils.helper_methods import get_plaintext_password, get_username_data
from src.postgres.password_manager import PasswordError


@pytest.mark.usefixtures("data_populator")
class TestPasswordManager:
    def test_passwords_get_hashed(self):
        """tests that password stored in database is hashed"""
        username = "N Bomb"
        raw_password = get_plaintext_password(username)
        salt = get_username_data(username, "salt")
        encrypted_password = get_username_data(username, "password")

        assert raw_password + salt != encrypted_password

    def test_authenticate_works_true(self, password_manager):
        """tests that a proper password authenticates the user"""
        username = "N Bomb"
        pw = get_plaintext_password(username)
        assert password_manager.authenticate_with_password(username, pw) > -1

    def test_authenticate_works_false(self, password_manager):
        """tests that a bad password is rejected"""
        username = "N Bomb"
        pw = get_plaintext_password(username) + " "
        with pytest.raises(PasswordError):
            password_manager.authenticate_with_password(username, pw)

    def test_change_password_bad_initial_password(self, password_manager):
        """tests that you get a permission error on a bad old_password"""
        username = "N Bomb"
        old_pass = "this is wrong"
        new_pass = "password1234"
        with pytest.raises(PasswordError):
            password_manager.change_password(username, old_pass, new_pass)

    def test_change_password_good_password(self, password_manager):
        """tests that you can change a password when the correct password is provided"""
        username = "N Bomb"
        old_pw = get_plaintext_password(username)
        assert password_manager.authenticate_with_password(username, old_pw) > -1

        new_pw = "password1234"
        password_manager.change_password(username, old_pw, new_pw)

        with pytest.raises(PasswordError):
            password_manager.authenticate_with_password(username, old_pw)
        assert password_manager.authenticate_with_password(username, new_pw) > -1

    @pytest.mark.usefixtures("add_common_passwords")
    @pytest.mark.parametrize(
        "password",
        [
            "12345",  # too short
            "manchester",  # in common_passwords.txt file
            "this is a long and secure sentence",  # has spaces
        ],
    )
    def test_validate_password_fails(self, password_manager, password):
        """tests that all prohibited passwords are not allowed"""
        with pytest.raises(ValueError):
            password_manager.validate_password(password)

    @pytest.mark.usefixtures("add_common_passwords")
    def test_validate_password_works(self, password_manager):
        """tests that a long, strong password can be used"""
        password = "184590fhjklasdfUIFSJh"
        password_manager.validate_password(password)
