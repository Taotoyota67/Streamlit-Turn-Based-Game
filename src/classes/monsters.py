import random
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
    def image(self) -> bytes:
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
        self._monsters: Dict[str, Monster] = {}
        self.load_monster()

    def load_monster(self) -> None:
        for monster, setting in config.MONSTERS.items():
            self._monsters[monster] = Monster(
                name=monster, **setting
            )

    def get(self, monster: str) -> Monster:
        return self._monsters[monster]
