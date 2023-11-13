from typing import Optional


class Stat:
    def __init__(self, value: int) -> None:
        self.__value = value

    def get(self) -> int:
        return self.__value

    def set(self, value: int) -> None:
        self.__value = value

    def increase(self, value: int, max_value: Optional[int] = None) -> None:
        if not max_value:
            max_value = int('inf')

        self.__value = min(self.__value + value, max_value)

    def reduce(self, value: int, min_value: Optional[int] = None) -> None:
        if not min_value:
            min_value = int("-inf")

        self.__value = max(self.__value - value, min_value)


class Stats:
    def __init__(self, **kwargs) -> None:
        health = kwargs.get("health", 0)
        self._health = Stat(health)
        self._max_health = Stat(health)

        self._damage = Stat(kwargs.get("damage", 0))

        mana = kwargs.get("mana", 0)
        self._mana = Stat(mana)
        self._max_mana = Stat(mana)

    def get(self, stat_name: str) -> int:
        stat: Stat = getattr(self, "_" + stat_name)
        return stat.get()

    @property
    def health(self) -> Stat:
        return self._health

    @property
    def max_health(self) -> Stat:
        return self._max_health

    @property
    def damage(self) -> Stat:
        return self._damage

    @property
    def mana(self) -> Stat:
        return self._mana

    @property
    def max_mana(self) -> Stat:
        return self._max_mana

    def serialize(self) -> dict:
        return {
            "damage": self.get("damage"),
            "health": self.get("health"),
            "maxHealth": self.get("max_health"),
            "mana": self.get("mana"),
            "maxMana": self.get("max_man")
        }
