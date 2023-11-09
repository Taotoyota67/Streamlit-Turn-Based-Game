import hashlib
import uuid

from db import db


def hash_sha256(text: str, salt: str) -> str:
    return hashlib.sha512(bytes(text + salt, 'utf-8')).hexdigest()


def generate_salt() -> str:
    return uuid.uuid4().hex


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
        """Check if username is valid or not with 5 rules
        1. Is not empty space.
        2. Is ascii.
        3. At least 4 letters long.
        4. Not already exists.

        Args:
            username (str): username to check.

        Returns:
            bool: username is valid.
        """
        return (
            username.isspace() or
            not username.isalnum() or
            not username.isascii() or
            username.isnumeric() or
            len(username) < 4 or
            self.has(username)
        )

    def has(self, username: str) -> bool:
        """Check if username already exists or not.

        Args:
            username (str): username.

        Returns:
            bool: username exists.
        """
        return username.lower() in db["accounts"]

    def add(self, username: str, password: str) -> None:
        """Add account to accounts system.

        Args:
            username (str): username
            password (str): password

        Raises:
            AccountAlreadyExists: when account already exists
        """
        if self.has(username):  # Just making sure.
            raise AccountAlreadyExists

        salt = generate_salt()

        db["accounts"][username.lower()] = [hash_sha256(password, salt), salt]
        db.save()

    def login(self, username: str, password: str) -> bool:
        """Login using username and password.
        *WARNING* not a good implementation of login system.

        Args:
            username (str): username
            password (str): password

        Returns:
            bool: login success.
        """
        if not self.has(username):
            return False

        password_hash, salt = db["accounts"][username.lower()]

        return password_hash == hash_sha256(password, salt)
