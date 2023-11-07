import json
from typing import Any, TypeVar, Type


T = TypeVar("T", bound="Database")


class Database:
    _instance = None
    # why tf do I use json?

    @classmethod
    def get(cls: Type[T]) -> "Database":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def load(self):
        with open("data/save.json", "r") as f:
            self._data: dict[str, Any] = json.load(f)

    def save(self):
        with open("data/save.json", "w") as f:
            json.dump(self._data, f, indent=4)

    def check_load(self):
        if not hasattr(self, "_data"):
            self.load()

    def __getitem__(self, __name: str) -> Any:
        self.check_load()
        return self._data[__name]

    def __setitem__(self, __name: str, __value: Any) -> None:
        self.check_load()
        self._data[__name] = __value
        # self.save()

    def __contains__(self, item: str) -> bool:
        self.check_load()
        return item in self._data

    def __delitem__(self, key: str) -> None:
        self.check_load()
        del self._data[key]


db = Database.get()
