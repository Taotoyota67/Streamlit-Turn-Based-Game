import random
from typing import Optional


class Text:
    def __init__(self, texts: Optional[list[str]] = None) -> None:
        if not texts:
            texts = []

        self.texts = texts

    def add(self, txt: str) -> "Text":
        """Add a text.

        Args:
            txt (str): The TEXT.

        Returns:
            Text: The Text class itself.
        """
        self.texts.append(txt)
        return self

    def adds(self, list_txt: list[str]) -> None:
        """Add texts using a list of string.

        Args:
            list_txt (list[str]): List of text.
        """
        self.texts += list_txt

    def choice(self) -> str:
        """Random text.

        Returns:
            str: Randomed text.
        """
        return random.choice(self.texts)


class EntityText:
    def __init__(self) -> None:
        self.texts: dict[str, Text] = {}

    def set(self, key: str, value: Text) -> None:
        """Set text by key.

        Args:
            key (str): The key.
            value (Text): The Text.
        """
        self.texts[key] = value

    def get(self, key: str) -> str:
        """Get the text from key. (Auto random)

        Args:
            key (str): The key.

        Raises:
            KeyError: You suck.

        Returns:
            str: Yo, the text is here.
        """
        if key not in self.texts:
            raise KeyError(f"Unknown EntityText key: {key}")

        return self.texts[key].choice()
