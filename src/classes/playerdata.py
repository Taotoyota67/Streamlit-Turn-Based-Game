from typing import Any
from db import db


class PlayerData:
    def __init__(self, username: str) -> None:
        self.username = username
        self.init_db()

    def init_db(self):
        if "users" not in db:
            db["users"] = {}

        if self.username not in db["users"]:
            db["users"][self.username] = {}
            db.save()

    def save(self) -> None:
        """Save data to database.
        """
        db.save()

    def delete(self):
        """Delete all player data.
        """
        del db["users"][self.username]
        db.save()

    def __getitem__(self, __name: str) -> Any:
        return db["users"][self.username][__name]

    def __setitem__(self, __name: str, __value: Any) -> None:
        db["users"][self.username][__name] = __value
