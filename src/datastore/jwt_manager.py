import jwt
from typing import NamedTuple
from datetime import datetime


class Token(NamedTuple):
    iat: datetime
    exp: datetime
    username: str
    level: int


class JWTManager:
    def __init__(self, key: str):
        self.key: str = key

    def create_jwt_token(self, username: str) -> Token:
        pass

    def validate_jwt_token(self, token: Token) -> None:
        pass

    def refresh_jwt_token(self, token: Token) -> Token:
        pass
