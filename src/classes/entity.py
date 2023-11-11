from typing import TypeVar, Optional

from classes.text import EntityText
from classes.skills import Buff, Poison

T = TypeVar("T", bound="Entity")


class Entity:
    def __init__(self, **kwargs) -> None:
        """Initialize when enter a combat.

        Kwargs:
            damage (float): entity damage.
            hp (float): entity health.
            mana (float): entity mana.
        """
        self.damage = kwargs.get("damage", 0)

        hp = kwargs.get("health", 0)
        self.health = hp
        self.max_health = hp

        mana = kwargs.get("mana", 0)
        self.mana = mana
        self.max_mana = mana

        self._poisons: list[Poison] = []  # [[duration, value]
        self._buffs: list[Buff] = []
        self._stun: int = 0

        self.name = kwargs.get("name", None)
        self.text = EntityText()

    def is_alive(self) -> bool:
        """Is entity alive?

        Returns:
            bool: alive.
        """
        return self.health > 0

    def serialize(self) -> dict:
        return {
            "damage": self.damage,
            "health": self.health,
            "maxHealth": self.max_health,
            "mana": self.mana,
            "maxMana": self.max_mana,
            "poisons": [[i.duration, i.damage] for i in self._poisons],
            "stun": self._stun
        }

    def tick(self) -> None:
        """Applied one tick of combat state. (Poison, Mana regen, etc.)
        """
        # Increase mana by 1 every turns.
        self.increase_mana(1)

        for index, poison in enumerate(self._poisons):
            # Take effect
            self.reduce_health(poison.damage)

            # Reduce poison turns
            self._poisons[index].duration -= 1

        # Clear out poison if duration ran out
        self._clear_ran_out()

        # Remove stun
        # if self.is_stun:
        self._stun = max(self._stun - 1, 0)

    def stun(self) -> None:
        """Stun this entity.
        """
        self._stun = 2

    def can_move(self) -> bool:
        """Can this entity make a move?

        Returns:
            bool: Yes or Nah
        """
        return (not self._stun) and self.is_alive()

    def add_poison(self, duration: int, value: int) -> None:
        """Add poison to an entity

        Args:
            duration (int): How long is the poison? (turns)
            value (int): damage per turn
        """
        self._poisons.append(Poison(duration, value))

    def add_buff(self, duration: int, multiplier: float) -> None:
        self._buffs.append(Buff(duration, multiplier))

    def clear_poisons(self) -> None:
        """Clear all poisons.
        """
        self._poisons = []

    def clear_buffs(self) -> None:
        """Clear all buffs.
        """
        self._buffs = []

    def _clear_ran_out(self) -> None:
        """Clear ran out effects (buff, poison).
        """
        self._poisons = [i for i in self._poisons if i.duration > 0]
        self._buffs = [i for i in self._buffs if i.duration > 0]

    def set_health(self, health: int) -> None:
        """Set entity current health. (Cannot exceed max health)

        Args:
            health (int): amount of health.
        """
        self.health = min(health, self.max_health)

    def set_max_health(self, health: int) -> None:
        """Set entity max health (will NOT change current health)

        Args:
            health (int): amount of health.
        """
        self.max_health = health

    def get_heal_amount(self) -> int:
        raise NotImplementedError

    def increase_health(self, amount: int) -> None:
        """Increase entity current health. (Cannot exceed max health)

        Args:
            amount (int): amount of health to increase.
        """
        self.health = min(self.health + amount, self.max_health)

    def increase_max_health(self, amount: int) -> None:
        """Increase entity max health (Will also increase current health)

        Args:
            amount (int): amount of health to increase.
        """
        self.max_health += amount
        self.health += amount

    def reduce_health(self, amount: int) -> None:
        """Reduce entity current health (Will not goes below 0)

        Args:
            amount (int): amount of health to reduce.
        """
        self.health = max(self.health - amount, 0)

    def reduce_max_health(self, amount: int) -> None:
        """Reduce entity max health.
        Max health will not go below 1.
        (Will also reduce current health, entity will not die from this)

        Args:
            amount (int): amount of max health to reduce.
        """
        self.max_health = max(self.max_health - amount, 1)
        self.health = max(self.health - amount, self.max_health)

    def set_mana(self, mana: int) -> None:
        """Set entity current mana. (Will not exceed max mana)

        Args:
            mana (int): amount of mana.
        """
        self.mana = min(mana, self.max_mana)

    def set_max_mana(self, mana: int) -> None:
        """Set entity max mana (Will NOT change current mana)

        Args:
            mana (int): amount of mana.
        """
        self.max_mana = mana

    def increase_mana(self, amount: int) -> None:
        """Increase entity current mana (Will not exceed max_mana)

        Args:
            amount (int): amount of mana.
        """
        self.mana = min(self.mana + amount, self.max_mana)

    def increase_max_mana(self, amount: int) -> None:
        """Increase entity max mana (Will also increase current mana)

        Args:
            amount (int): amount of mana.
        """
        self.max_mana += amount
        self.mana += amount

    def reduce_mana(self, amount: int) -> None:
        """Reduce entity current mana (Will not goes below 0)

        Args:
            amount (int): _description_
        """
        self.mana = max(self.mana - amount, 0)

    def reduce_max_mana(self, amount: int) -> None:
        """Reduce entity max mana.
        Max mana will not goes below 0
        (Will also reduce current mana, will not goes below max mana.)

        Args:
            amount (int): _description_
        """
        self.max_mana = max(self.max_mana - amount, 0)
        self.mana = max(self.mana - amount, self.max_mana)

    def get_damage(self) -> int:
        damage = self.damage

        for buff in self._buffs:
            damage *= buff.multiplier

        return int(damage)

    def attack(self, target: "Entity", damage: Optional[int] = None) -> int:
        """Attack an entity. (Never pass in a damage! For backend only!)

        Args:
            target (Entity): entity to attack
            damage (Optional[int], optional): amount of damage. (DONT USE THIS)

        Returns:
            int: damage dealt
        """
        if not damage:
            damage = self.get_damage()

        target.reduce_health(damage)

        return damage
