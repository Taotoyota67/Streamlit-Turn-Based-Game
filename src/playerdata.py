from typing import Any
from db import Database

class PlayerData:
    def __init__(self, username: str, db: Database) -> None:
        self.username = username
        self.db = db

    def __getitem__(self, __name: str) -> Any:
        return self.db["users"][self.username][__name]
    
    def __setitem__(self, __name: str, __value: Any) -> None:
        self.db["users"][self.username][__name] = __value
        self.db.save()
