import random
from typing import Optional


class Text:
    def __init__(self, texts: Optional[list[str]] = None) -> None:
        if not texts:
            texts = []

        self.texts = texts

    def add(self, txt: str) -> "Text":
        self.texts.append(txt)
        return self

    def adds(self, list_txt: list[str]) -> None:
        self.texts += list_txt

    def choice(self) -> str:
        return random.choice(self.texts)


class EntityText:
    def __init__(self) -> None:
        self.texts: dict[str, Text] = {}

    def set(self, key: str, value: Text) -> None:
        self.texts[key] = value

    def get(self, key: str) -> str:
        if key not in self.texts:
            raise KeyError(f"Unknown EntityText key: {key}")

        return self.texts[key].choice()
