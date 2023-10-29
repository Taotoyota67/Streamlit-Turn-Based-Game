import json
from typing import Any


class Database:
    # why tf do I use json?
    def __init__(self):
        self._data = json.load(open("data/save.json"))

    def save(self):
        json.dump(self._data, open("data/save.json", "w"), indent=4)

    def __getitem__(self, __name: str) -> Any:
        return self._data.get(__name)

    def __setitem__(self, __name: str, __value: Any) -> None:
        self._data[__name] = __value
        self.save()
