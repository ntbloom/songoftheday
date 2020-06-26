import jwt
from typing import NamedTuple, Optional
from time import time
from src import JWT_DAYS_VALID, TEST_JWT_ALGO


class JWTError(Exception):
    """
    Generic exception to fail either decryption or validation of jwt
    """

    def __init__(self):
        self.message = "Invalid JSON Web Token"
        super().__init__(self.message)


class Token(NamedTuple):
    usr: str  # matches username in postgres
    lev: int  # level: 0 = user, 1 = administrator
    iat: Optional[float] = time()  # time issued
    exp: Optional[float] = iat + (JWT_DAYS_VALID * 86400)  # expiration


class JWTManager:
    def __init__(self, key: str, algorithm: Optional[str] = "HS512"):
        self.key: str = key
        self.algorithm = algorithm

    def encrypt(self, token: Token) -> str:
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
            return Token(t["usr"], t["lev"], t["iat"], t["exp"])
        except jwt.exceptions.DecodeError:
            raise JWTError()
        except jwt.exceptions.InvalidAlgorithmError:
            raise JWTError()

    def validate(self, token: Token) -> None:

        pass
