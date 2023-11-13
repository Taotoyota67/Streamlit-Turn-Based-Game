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
        self.health = Stat(health)
        self.max_health = Stat(health)

        self.damage = Stat(kwargs.get("damage", 0))

        mana = kwargs.get("mana", 0)
        self.mana = Stat(mana)
        self.max_mana = Stat(mana)

    def get(self, stat_name: str) -> int:
        stat: Stat = getattr(self, stat_name)
        return stat.get()

    def serialize(self) -> dict:
        return {
            "damage": self.get("damage"),
            "health": self.get("health"),
            "maxHealth": self.get("max_health"),
            "mana": self.get("mana"),
            "maxMana": self.get("max_man")
        }
