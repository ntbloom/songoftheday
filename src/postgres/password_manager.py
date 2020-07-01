from src.postgres.postgres_connector import PostgresConnector
from argon2 import argon2_hash
from secrets import token_urlsafe
from src import SALT_LENGTH, MIN_PW_LENGTH


class PasswordError(Exception):
    def __init__(self):
        self.message = "Invalid Password"
        super().__init__(self.message)


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
        Changes the user's password if authentication passes and new password is legal
        """
        self.authenticate_with_password(username, old_pw)
        self.validate_password(new_pw)

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

    def authenticate_with_password(self, username: str, plaintext_password: str) -> int:
        """
        Attempts to authenticate user, returns authority level.
        if auth fails: -> raise PasswordError
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
        if results is None:  # username doesn't exist
            raise PasswordError
        encrypted_password = results[0]
        salt = results[1]
        administrator = results[2] == "True"
        hashed = PasswordManager.hash(plaintext_password, salt)
        if encrypted_password != hashed:
            raise PasswordError
        if administrator:
            return 1
        return 0

    def _is_weak(self, pw: str) -> bool:
        """returns True if pw in common_passwords table"""
        self.cursor.execute(
            """
            SELECT password 
            FROM common_passwords
            WHERE password = %s
            """,
            (pw,),
        )
        result = self.cursor.fetchone()
        return result is not None

    def validate_password(self, password: str) -> None:
        """
        Raises ValueError exception for insecure passwords
        """
        if len(password) < MIN_PW_LENGTH:
            raise ValueError("password is too short")
        if self._is_weak(password) is True:
            raise ValueError("password is too common")
        if " " in password:
            raise ValueError("no spaces alllowed")
