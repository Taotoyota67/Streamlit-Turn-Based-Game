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
        if not db["accounts"]:  # pylint: disable=E1136
            db["accounts"] = {}  # pylint: disable=E1137

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
        return username.lower() in db["accounts"]  # pylint: disable=E1136

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
        # pylint: disable=E1136
        db["accounts"][username.lower()] = hash_sha256(password)
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
        # pylint: disable=E1136
        return db["accounts"][username.lower()] == hash_sha256(password) and self.has(username)
