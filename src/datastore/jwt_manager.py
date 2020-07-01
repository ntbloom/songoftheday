import jwt
from jwt.exceptions import DecodeError, InvalidAlgorithmError
from typing import NamedTuple, Callable
from time import time
from src import JWT_DAYS_VALID
import functools


class JWTError(Exception):
    """
    Generic exception to fail either decryption or validation of jwt
    """

    def __init__(self, reason):
        self.message = f"Invalid JSON Web Token: {reason}"
        super().__init__(self.message)


class Token(NamedTuple):
    usr: str  # matches username in postgres
    lev: int  # level: 0 = user, 1 = administrator
    iat: float = time()  # time issued
    exp: float = time() + (JWT_DAYS_VALID * 86400)  # expiration


class JWTManager:
    def __init__(self, key: str, algorithm: str = "HS512"):
        self.key: str = key
        self.algorithm = algorithm

    def encrypt(self, token: Token) -> bytes:
        """
        Encrypt the token and return a string
        """
        return jwt.encode(token._asdict(), self.key, self.algorithm)

    def decrypt(self, encrypted: str) -> Token:
        """
        Decrypt the encrypted token, return a Token object
        """
        try:
            t = jwt.decode(encrypted, self.key, algorithms=self.algorithm)
            return Token(**t)
        except DecodeError as e:
            raise JWTError(f"problem decoding: {e}")
        except InvalidAlgorithmError as e:
            raise JWTError(f"invalid algorithm: {e}")

    def validate(self, encrypted: str) -> Token:
        """
        Validate and return decrypted token.  Raises JWTError on invalid token
        """
        token = self.decrypt(encrypted)
        now = time()

        # reject if issued at is in the future
        if token.iat > now:
            raise JWTError("issued at is in the future")

        # reject if token is expired
        if token.exp < now:
            raise JWTError("token is expired")

        return token
