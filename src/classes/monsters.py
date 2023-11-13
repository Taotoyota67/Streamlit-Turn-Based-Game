import random
from typing import Dict

import config
from classes.entity import Entity
from classes.player import Player
from classes.text import Text
from classes.image import Image


class MonsterInvalidMove(Exception):
    """Invalid move for monster"""


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

    def set_text(self, key: str, value: list[str]) -> None:
        self.text.set(
            key,
            Text(value)
        )

    def random_move(self) -> str:
        """Random move from monster, edit at config.py

        Returns:
            str: move
        """
        weights = list(self.moves.values())
        moves = list(self.moves.keys())

        return random.choices(moves, weights=weights)[0]

    def get_heal_amount(self) -> int:
        """Get heal amount (Settings in config.py)

        Returns:
            int: _description_
        """
        return int(config.MONSTER_HEAL_MULTIPLIER * self.stats.get("max_health"))

    def make_move(self, move: str, player: Player) -> int:
        """"Make monster do a move. Please use `random_move` method and pass it to here.

        Args:
            move (str): move from `random_move`
            player (Player): game.player

        Raises:
            MonsterInvalidMove: make an invalid move.

        Returns:
            int: attack -> amount of damage
                 heal -> amount of heal
                 damage_buff -> amount of damage
                 mana_drain -> amount of mana
                 stun -> 1 (yes, just 1)

        """
        if move == "attack":
            return self.attack(player.entity)
        if move == "heal":
            heal = self.get_heal_amount()
            self.stats.health.increase(heal, self.stats.get("max_health"))
            return heal
        if move == "damage_buff":
            damage = self.get_damage() * config.MONSTER_DAMAGE_MULTIPLIER
            self.attack(player.entity, damage=damage)
            return damage
        if move == "mana_drain":
            mana_amount = int(player.stats.get("max_mana") *
                              config.MONSTER_MANA_DRAIN_MULTIPLIER)
            player.stats.mana.reduce(mana_amount)
            return mana_amount
        if move == "stun":
            player.entity.stun()
            return 1

        raise MonsterInvalidMove


class Monsters:
    def __init__(self) -> None:
        self._monsters = {}
        self.load_monster()

    def load_monster(self) -> None:
        for monster, setting in config.MONSTERS.items():
            self._monsters[monster] = Monster(
                **setting
            )

    def get(self, monster: str) -> Monster:
        return self._monsters[monster]
