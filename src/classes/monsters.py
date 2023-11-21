import random
from io import BytesIO
from typing import Dict

import config
from classes.entity import Entity
from classes.enums import MoveType
from classes.image import Image
from classes.text import Text


class Monster(Entity):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.moves: Dict[str, int] = kwargs.get("moves", {})

        texts = kwargs.get("texts", {})
        for key, value in texts.items():
            self.set_text(key, value)

        image = kwargs.get("image", {})
        self._image = Image()
        self._image["alive"] = image["alive"]
        self._image["dead"] = image["dead"]

    @property
    def image(self) -> BytesIO:
        return self._image["alive"] if self.is_alive() else self._image["dead"]

    def serialize(self) -> dict:
        return {
            "name": self.name,
            "entity": super().serialize()
        }

    def set_text(self, key: str, value: list[str]) -> None:
        self.text.set(
            key,
            Text(value)
        )

    def random_move(self) -> MoveType:
        """Random move from monster, edit at config.py

        Returns:
            MoveType: game.enums.MoveType
        """
        weights = list(self.moves.values())
        moves = [MoveType[i.upper()] for i in self.moves.keys()]

        return random.choices(moves, weights=weights)[0]


class Monsters:
    def __init__(self) -> None:
        self.__monsters = config.MONSTERS

    def get_all_names(self) -> list[str]:
        """Get all monster names.

        Returns:
            list[str]: List of monster names.
        """
        return list(self.__monsters.keys())

    def get(self, monster: str) -> Monster:
        """Get/Summon the monster by name.

        Args:
            monster (str): Monster name.

        Raises:
            NameError: No monster found.

        Returns:
            Monster: A monster object.
        """
        if monster in self.__monsters:
            return Monster(
                name=monster, **self.__monsters[monster]
            )

        raise NameError(f"Monster not found; {monster}")
