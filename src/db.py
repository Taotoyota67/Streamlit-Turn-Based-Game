import json
from typing import Any, TypeVar, Type


T = TypeVar("T", bound="Database")


class Database:
    _instance = None
    # why tf do I use json?

    def __new__(cls: Type[T]) -> "Database":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(Database._instance, "_data"):
            with open("data/save.json", "r") as f:
                self._data = json.load(f)

    def save(self):
        with open("data/save.json", "w") as f:
            json.dump(self._data, f, indent=4)

    def __getitem__(self, __name: str) -> Any:
        return self._data[__name]

    def __setitem__(self, __name: str, __value: Any) -> None:
        self._data[__name] = __value

    def __contains__(self, item: str) -> bool:
        return item in self._data

    def __delitem__(self, key: str) -> None:
        del self._data[key]


db = Database()
