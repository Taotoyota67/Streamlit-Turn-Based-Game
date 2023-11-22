from typing import Optional, TypeVar

import config
from classes.enums import MoveType
from classes.errors import CannotMove, InvalidMove, AlreadyDead
from classes.skills import Poison
from classes.stats import Stats
from classes.text import EntityText

T = TypeVar("T", bound="Entity")


class Entity:
    def __init__(self, **kwargs) -> None:
        """Initialize when enter a combat.

        Kwargs:
            damage (float): entity damage.
            hp (float): entity health.
            mana (float): entity mana.
        """
        stats = kwargs.get("stats", None)
        if stats:
            self.stats: Stats = stats
        else:
            self.stats = Stats(**kwargs)

        self._is_player = kwargs.get("is_player", False)
        self._poisons: list[Poison] = []  # [[duration, value]
        self._stun: int = 0

        self.name = kwargs.get("name", None)
        self.text = EntityText()

    def serialize(self) -> dict:
        return {
            "stats": self.stats.serialize(),
            "poisons": [[i.duration, i.multiplier] for i in self._poisons],
            "stun": self._stun
        }

    def is_alive(self) -> bool:
        """Is entity alive?

        Returns:
            bool: alive.
        """
        return self.stats.get("health") > 0

    def is_stun(self) -> bool:
        """Is this entity stun?

        Returns:
            bool: Yes or Nah.
        """
        return bool(self._stun)

    def is_poison(self) -> bool:
        """Is this entity has poison?

        Returns:
            bool: Ye or na.
        """
        return bool(self._poisons)

    def tick(self) -> None:
        """Applied a tick of combat state. (Poison, Mana regen, etc.)

        Raises:
            AlreadyDead: This entity is ALREADY DEAD.
        """
        if not self.is_alive():
            raise AlreadyDead(
                "This entity is already dead. Did you forget to check by using `is_alive()`?"
            )

        # Increase mana by 1 every turns
        self.stats.mana.increase(1, self.stats.get('max_mana'))

        for index, poison in enumerate(self._poisons):
            # Take effect
            damage = int(self.stats.get("max_health") * poison.multiplier)
            self.stats.health.reduce(damage, 0)

            # Reduce poison turns
            self._poisons[index].duration -= 1

        # Clear out poison if duration ran out
        self._clear_ran_out()

        # Reduce stun
        self._stun = max(self._stun - 1, 0)

    def stun(self) -> None:
        """Stun this entity.
        """
        self._stun = 2

    def add_poison(self, duration: int, multiplier: float) -> None:
        """Add poison to an entity.

        Args:
            duration (int): How long is the poison? (turns)
            multiplier (float): Damage% of max health per turn.
        """
        self._poisons.append(Poison(duration, multiplier))

    def clear_poisons(self) -> None:
        """Clear all poisons.
        """
        self._poisons = []

    def _clear_ran_out(self) -> None:
        """Clear ran out effects (poison).
        """
        self._poisons = [i for i in self._poisons if i.duration > 0]

    def get_damage(self) -> int:
        """Get damage, Call this function before `attack`.

        Returns:
            int: Amount of damage.
        """
        return self.stats.damage.get()

    def get_heal_multiplier(self) -> float:
        if self._is_player:
            return config.PLAYER_HEAL_MULTIPLIER
        return config.MONSTER_HEAL_MULTIPLIER

    def attack(self, target: "Entity", damage: Optional[int] = None) -> int:
        """Attack an entity. (Never pass in a damage! For backend only!)

        Args:
            target (Entity): Entity to attack.
            damage (Optional[int], optional): Amount of damage. (DONT USE THIS)

        Returns:
            int: Damage dealt.
        """
        if not damage:
            damage = self.get_damage()

        target.stats.health.reduce(damage, 0)

        return damage

    def make_move(self, move: MoveType, target: "Entity") -> int:
        """Make a move.

        Args:
            move (MoveType): Enums from game.enums.MoveType
            target (Entity): Target of the move. (If heal, still put monster.)

        Raises:
            CannotMove: Entity is stunned or already dead.
            InvalidMove: Unknown move.

        Returns:
            int: Amount of damage, Amount of heal, Poison durations or 1 for Stun.
        """
        if self.is_stun() or not self.is_alive():
            raise CannotMove(
                "This entity is either stunned or already dead."
            )

        ret = 0

        if move == MoveType.ATTACK:
            ret = self.attack(target)
        elif move == MoveType.DAMAGE_BUFF:
            ret = self.attack(target, self.get_damage() * 2)
        elif move == MoveType.HEAL:
            max_health = self.stats.get("max_health")
            ret = int(max_health * self.get_heal_multiplier())
            self.stats.health.increase(ret, self.stats.get("max_health"))
        elif move == MoveType.POISON:
            target.add_poison(
                config.POISON_DURATION,
                config.POISON_MULTIPLIER
            )
            ret = config.POISON_DURATION
        elif move == MoveType.LIFE_STEAL:
            damage = self.attack(target)
            self.stats.health.increase(
                damage,
                self.stats.get("max_health")
            )
            ret = damage
        elif move == MoveType.STUN:
            target.stun()
            ret = 1
        elif move == MoveType.MANA_DRAIN:
            mana_amount = int(target.stats.get("max_mana") *
                              config.MONSTER_MANA_DRAIN_MULTIPLIER)
            target.stats.mana.reduce(mana_amount, 0)
            ret = mana_amount
        else:
            raise InvalidMove("Could not recognize `MoveType`.")

        return ret
