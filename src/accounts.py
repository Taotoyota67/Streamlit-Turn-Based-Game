from db import Database
from utils.functions import hash_sha256


class AccountAlreadyExists(Exception):
    """Account already exists"""


class AccountNotExists(Exception):
    """Account not exists"""


class Accounts:
    def __init__(self, db: Database) -> None:
        self.db = db
        self.init_db()

    def init_db(self):
        if not self.db["accounts"]:
            self.db["accounts"] = {}

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
        return username.lower() in self.db["accounts"]

    def add(self, username: str, password: str) -> None:
        if self.has(username):  # Just making sure.
            raise AccountAlreadyExists
        password = hash_sha256(password)
        self.db["accounts"][username.lower()] = password
        self.db.save()

    def login(self, username: str, password: str) -> bool:
        if not self.has(username):
            raise AccountNotExists
        password = hash_sha256(password)
        return self.db["accounts"][username.lower()] == password
