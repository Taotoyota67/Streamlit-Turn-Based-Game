from .playerdata import PlayerData  # pylint: disable=E0402
from .entity import CombatStats  # pylint: disable=E0402

from typing import Optional


class PlayerException(Exception):
    """Player Exceptions"""


class PlayerAlreadyInCombat(PlayerException):
    """Player already in combat!"""


class PlayerNotInCombat(PlayerException):
    """Player is not in combat!"""


class PlayerStats:
    def __init__(self):
        self.reset_stats()

    @property
    def damage(self) -> float:
        return self._damage

    @property
    def defense(self) -> float:
        return self._defense

    @property
    def health(self) -> float:
        return self._health

    @property
    def mana(self) -> float:
        return self._mana

    def reset_stats(self):
        self._damage = 10
        self._defense = 0
        self._health = 100
        self._mana = 100

    def set_damage(self, damage: float) -> None:
        self._damage = damage  # pylint: disable=W0201

    def set_defense(self, defense: float) -> None:
        self._defense = defense  # pylint: disable=W0201

    def set_health(self, health: float) -> None:
        self._health = health  # pylint: disable=W0201

    def set_mana(self, mana: float) -> None:
        self._mana = mana  # pylint: disable=W0201


class Player:
    def __init__(self, username: str) -> None:
        self._username = username
        self._pdata = PlayerData(username)
        self._stats = PlayerStats()
        self._combat: Optional[CombatStats] = None

    @property
    def username(self) -> str:
        return self._username

    @property
    def stats(self) -> PlayerStats:
        return self._stats

    @property
    def combat(self) -> Optional[CombatStats]:
        return self._combat

    @property
    def is_alive(self) -> bool:
        if self._combat is None:
            raise PlayerNotInCombat("Player is not in combat!")
        return self._combat.is_alive

    def start_combat(self) -> None:
        if self._combat is not None:
            raise PlayerAlreadyInCombat("Player is already in combat!")

        self._combat = CombatStats(
            damage=self._stats.damage,
            health=self._stats.health,
            defense=self._stats.defense,
            mana=self._stats.mana,
        )

    def leave_combat(self) -> None:
        if self._combat is None:
            raise PlayerNotInCombat("Player is not in combat!")

        self._combat = None


# game.monster.spawn(game.entity.Slime)
# game.player.startCombat()
# player.stats
# player.combat
# game.player.
