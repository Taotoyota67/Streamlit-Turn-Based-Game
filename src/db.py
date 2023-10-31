import json
from typing import Any


class Database:
    # why tf do I use json?
    def __init__(self):
        with open("data/save.json") as f:
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
