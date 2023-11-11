from dataclasses import dataclass
from enum import Enum


class SkillType(Enum):
    BUFF = 0
    HEAL = 1
    POISON = 2
    LIFE_STEAL = 3
    STUN = 4


@dataclass
class Buff:
    duration: int
    multiplier: float


@dataclass
class Poison:
    duration: int
    damage: int
