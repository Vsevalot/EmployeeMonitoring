from os import urandom
from hashlib import pbkdf2_hmac
from typing import TypeAlias


HashedPassword: TypeAlias = bytes
Salt: TypeAlias = bytes


class PasswordService:
    @staticmethod
    def hash_password(
        password: str,
        salt: bytes | None = None,
        iterations=100000,
    ) -> tuple[HashedPassword, Salt]:
        if salt is None:
            salt = urandom(16)
        hashed_password = pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            iterations,
        )
        return hashed_password, salt
