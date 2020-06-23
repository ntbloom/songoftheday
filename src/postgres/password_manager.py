from src.postgres.postgres_connector import PostgresConnector
from argon2 import argon2_hash


class PasswordManager(PostgresConnector):
    def __init__(self, database: str, host: str):
        super().__init__(database, host)

    @staticmethod
    def hash(pw: str, salt: str) -> str:
        return argon2_hash(pw, salt)

    def create_new_password(self, username: str, old_pw: str, new_pw: str) -> None:
        """
        Creates a new password for the user
        """
        pass

    def authenticate(self, username: str, pw: str) -> bool:
        """
        Attempts to authenticate user, returns whether auth passed
        """

        pass

    def user_has_administrator_acces(self, username: str) -> bool:
        """
        Does the user have administrator access?
        """
        pass
