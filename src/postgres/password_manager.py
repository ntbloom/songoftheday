from src.postgres.postgres_connector import PostgresConnector
from argon2 import argon2_hash
from secrets import token_urlsafe
from src import SALT_LENGTH


class PasswordManager(PostgresConnector):
    def __init__(self, database: str, host: str):
        super().__init__(database, host)

    @staticmethod
    def hash(pw: str, salt: str) -> str:
        """
        Hash the password with salt using argon2 hashing algorithm
        """
        return str(argon2_hash(pw, salt))

    def change_password(self, username: str, old_pw: str, new_pw: str) -> None:
        """
        Changes the user's password if authentication passes
        """
        self.authenticate(username, old_pw)

        salt = token_urlsafe(SALT_LENGTH)
        new_hash = PasswordManager.hash(new_pw, salt)
        self.cursor.execute(
            """
            UPDATE users
            SET 
                password = %s,
                salt = %s
            WHERE username = %s 
        """,
            (new_hash, salt, username),
        )
        self.commit()

    def authenticate(self, username: str, plaintext_password: str) -> int:
        """
        Attempts to authenticate user, returns authority level.
        if auth fails: -> raise PermissionError
        if auth passes:
            if has_administrator_access: -> 1
            if not has_administrator_access: -> 0
        """
        self.cursor.execute(
            """
            SELECT 
                password, 
                salt,
                has_administrator_access
            FROM users
            WHERE username = %s
        """,
            (username,),
        )
        results = self.cursor.fetchone()
        encrypted_password = results[0]
        salt = results[1]
        administrator = results[2] == "True"
        hashed = PasswordManager.hash(plaintext_password, salt)
        if encrypted_password != hashed:
            raise PermissionError("invalid password")
        if administrator:
            return 1
        return 0
