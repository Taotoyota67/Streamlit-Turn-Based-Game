from classes.playerdata import PlayerData
from classes.entity import Entity


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

    def serialize(self) -> dict:
        return {
            "damage": self._damage,
            "defense": self._defense,
            "health": self._health,
            "mana": self._mana
        }

    def reset_stats(self):
        self._damage = 10
        self._defense = 0
        self._health = 100
        self._mana = 100

    def set_damage(self, damage: float) -> None:
        self._damage = damage  # pylint: disable=W0201 # (define variable outside __init__)

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
        self.entity = Entity(
            damage=self._stats.damage,
            health=self._stats.health,
            defense=self._stats.defense,
            mana=self._stats.mana,
        )

    @property
    def username(self) -> str:
        return self._username

    @property
    def stats(self) -> PlayerStats:
        return self._stats

    def save(self) -> None:
        """Save player.
        """
        self._pdata["playerStats"] = self._stats.serialize()
        self._pdata["playerCombat"] = self.entity.serialize()

        self._pdata.save()
