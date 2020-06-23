from src.postgres.postgres_connector import PostgresConnector
from argon2 import argon2_hash


class PasswordManager(PostgresConnector):
    def __init__(self, database: str, host: str):
        super().__init__(database, host)

    @staticmethod
    def hash(pw: str, salt: str) -> str:
        return str(argon2_hash(pw, salt))

    def change_password(self, username: str, old_pw: str, new_pw: str) -> None:
        """
        Changes the user password
        """
        pass

    def authenticate(self, username: str, plaintext_password: str) -> bool:
        """
        Attempts to authenticate user, returns whether auth passed
        """
        self.cursor.execute(
            """
            SELECT 
                password, 
                salt
            FROM users
            WHERE username = %s
        """,
            (username,),
        )
        results = self.cursor.fetchone()
        encrypted_password = results[0]
        salt = results[1]
        hashed = PasswordManager.hash(plaintext_password, salt)
        return encrypted_password == hashed

    def user_has_administrator_acces(self, username: str) -> bool:
        """
        Does the user have administrator access?
        """
        pass
