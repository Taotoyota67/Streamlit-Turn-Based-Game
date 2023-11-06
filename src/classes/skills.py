from enum import Enum
from .entity import Entity  # pylint: disable=E0402


class SkillType(Enum):
    HEAL = 0
    DAMAGE = 1


class Skill:
    def __init__(self,
                 skill_type: SkillType,
                 value: float,
                 duration: int = 0):
        """Replesent a skill in the game

        Args:
            skill_type (SkillType): A skill type
            value (float): Amount of dmg/heal
            duration (int): How long the skill lasts?
        """
        self._type = skill_type
        self._value = value
        self._duration = duration

    def cast(self, target: Entity) -> None:
        """Cast a skill to an entity.

        Args:
            other (Entity): target entity
        """
        if self._duration < 1:
            self._cast(target)
        else:
            self._inflict(target)

    def _cast(self, target: Entity) -> None:
        if self._type == SkillType.DAMAGE:
            target.reduce_health(self._value)
        elif self._type == SkillType.HEAL:
            target.increase_health(self._value)

    def _inflict(self, target: Entity) -> None:
        target.add_effect(
            self._duration,
            # Value will be negative if skill type is damage.
            self._value * (-1 * (self._type == SkillType.DAMAGE))
        )
