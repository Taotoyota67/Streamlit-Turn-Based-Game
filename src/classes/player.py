from classes.playerdata import PlayerData
from classes.entity import Entity
from classes.stats import Stats

import config


class PlayerException(Exception):
    """Player Exceptions"""


class PlayerAlreadyInCombat(PlayerException):
    """Player already in combat!"""


class PlayerNotInCombat(PlayerException):
    """Player is not in combat!"""


class Player:
    def __init__(self, username: str) -> None:
        self._username = username
        self._pdata = PlayerData(username)
        self.stats = Stats(**config.PLAYER_DEFAULT_STATS)
        self.entity = Entity(stats=self.stats)

    @property
    def username(self) -> str:
        return self._username

    def tick(self) -> None:
        return self.entity.tick()

    def is_alive(self) -> bool:
        return self.entity.is_alive()

    def is_poison(self) -> bool:
        return self.entity.is_poison()

    def is_stun(self) -> bool:
        return self.entity.is_stun()

    def attack(self, target: Entity) -> int:
        return self.entity.attack(target)

    def save(self) -> None:
        """Save player.
        """
        self._pdata["playerStats"] = self.stats.serialize()
        self._pdata["playerCombat"] = self.entity.serialize()

        self._pdata.save()
