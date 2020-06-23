import pytest
from tests.utils.helper_methods import get_plaintext_password, get_username_data


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
        assert password_manager.authenticate(username, pw) is True

    def test_authenticate_works_false(self, password_manager):
        """tests that a bad password is rejected"""
        username = "N Bomb"
        pw = get_plaintext_password(username) + " "
        assert password_manager.authenticate(username, pw) is False

    def test_change_password_bad_initial_password(self, password_manager):
        """tests that you get a permission error on a bad old_password"""
        username = "N Bomb"
        old_pass = "this is wrong"
        new_pass = "password1234"
        with pytest.raises(PermissionError):
            password_manager.change_password(username, old_pass, new_pass)

    # def test_change_password_good_password(self, password_manager):
    #     """tests that you can change a password when the correct password is provided"""
    #     username = "N Bomb"
    #     old_pw = get_plaintext_password(username)
    #     assert password_manager.authenticate(username, old_pw) is True
    #
    #     new_pw = "password1234"
    #     password_manager.change_password(username, old_pw, new_pw)
    #
    #     assert password_manager.authenticate(username, old_pw) is False
    #     assert password_manager.authenticate(username, new_pw) is True
