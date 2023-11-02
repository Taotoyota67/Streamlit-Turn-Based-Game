from db import db
from utils.functions import hash_sha256


class AccountAlreadyExists(Exception):
    """Account already exists"""


class AccountNotExists(Exception):
    """Account not exists"""


class Accounts:
    def __init__(self) -> None:
        self.init_db()

    def init_db(self):
        if not db["accounts"]:
            db["accounts"] = {}

    def check_username(self, username: str) -> bool:
        """Check if username bad or not."""
        return (
            username.isspace() or
            not username.isalnum() or
            not username.isascii() or
            len(username) < 4 or
            self.has(username)
        )

    def has(self, username: str) -> bool:
        """Check if username exists or not"""
        return username.lower() in db["accounts"]

    def add(self, username: str, password: str) -> None:
        if self.has(username):  # Just making sure.
            raise AccountAlreadyExists
        db["accounts"][username.lower()] = hash_sha256(password)
        db.save()

    def login(self, username: str, password: str) -> bool:
        return db["accounts"][username.lower()] == hash_sha256(password) and self.has(username)
