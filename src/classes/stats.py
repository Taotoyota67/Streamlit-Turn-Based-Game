from typing import Optional, Union

# Type checking wouldn't allow me to use `inf` which is a float.
# But the type annotation was int. So now we have this weird shit.
Number = Union[float, int]


class Stat:
    def __init__(self, value: int) -> None:
        self.__value = value

    def get(self) -> int:
        return int(self.__value)

    def set(self, value: int) -> None:
        self.__value = value

    def increase(self, value: int, max_value: Optional[Number] = None) -> None:
        """Increase the stat.

        Args:
            value (int): Increase amount.
            max_value (Optional[Number], optional): int. Defaults to None.
        """
        if not max_value:
            max_value = float('inf')

        self.__value = min(self.__value + value, max_value)

    def reduce(self, value: int, min_value: Optional[Number] = None) -> None:
        """Reduce the stat.

        Args:
            value (int): Reduce amount.
            min_value (Optional[Number], optional): int. Defaults to None.
        """
        if not min_value:
            min_value = float("-inf")

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
        """Get stat by name.

        Args:
            stat_name (str): Name of the stat.

        Returns:
            int: Stat value.
        """
        # This is a bad code. But it works.
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
