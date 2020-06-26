import jwt
from typing import NamedTuple
from time import time
from src import JWT_DAYS_VALID


class JWTError(Exception):
    def __init__(self):
        self.message = "Invalid JSON Web Token"
        super().__init__(self.message)


class Token(NamedTuple):
    username: str  # matches username in postgres
    level: int  # 0 = user, 1 = administrator
    iat: float = time()  # time issued
    exp: float = iat + (JWT_DAYS_VALID * 86400)


class JWTManager:
    def __init__(self, key: str):
        self.key: str = key

    def encrypt(self, token: Token) -> Token:
        pass

    def decrypt(self, token: Token) -> Token:
        pass

    def validate(self, token: Token) -> None:
        pass

    def refresh(self, token: Token) -> Token:
        pass
