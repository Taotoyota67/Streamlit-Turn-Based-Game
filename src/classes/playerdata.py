from typing import Any
from db import db


class PlayerData:
    def __init__(self, username: str) -> None:
        self.username = username
        self.init_db()

    def init_db(self):
        if "users" not in db:  # pylint: disable=E1135
            db["users"] = {}  # pylint: disable=E1137

        if self.username not in db["users"]:  # pylint: disable=E1136
            db["users"][self.username] = {}  # pylint: disable=E1136
            db.save()

    def delete(self):
        """Delete all player data.
        """
        del db["users"][self.username]  # pylint: disable=E1136
        db.save()

    def __getitem__(self, __name: str) -> Any:
        # pylint: disable=E1136
        return db["users"][self.username][__name]

    def __setitem__(self, __name: str, __value: Any) -> None:
        # pylint: disable=E1136
        db["users"][self.username][__name] = __value
        db.save()
