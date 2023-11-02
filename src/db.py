import json
from typing import Any, TypeVar, Type


T = TypeVar("T", bound="Database")


class Database:
    _instance = None
    # why tf do I use json?

    def __init__(self):
        raise RuntimeError("Call database using Database.get() only!")

    @classmethod
    def get(cls: Type[T]) -> T:
        if cls._instance is None:
            obj = cls.__new__(cls)
            print('create new')
            obj.init()
            cls._instance = obj
        print('ret')
        return cls._instance

    def init(self):
        with open("data/save.json", "r") as f:
            self._data = json.load(f)

    def save(self):
        with open("data/save.json", "w") as f:
            json.dump(self._data, f, indent=4)

    def __getitem__(self, __name: str) -> Any:
        return self._data[__name]

    def __setitem__(self, __name: str, __value: Any) -> None:
        self._data[__name] = __value
        self.save()

    def __contains__(self, item: str) -> bool:
        return item in self._data

    def __delitem__(self, key: str) -> None:
        del self._data[key]


db = Database.get()
