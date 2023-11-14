from enum import Enum


class MoveType(Enum):
    ATTACK = "attack"
    DAMAGE_BUFF = "damage_buff"
    HEAL = "heal"
    POISON = "poison"
    LIFE_STEAL = "life_steal"
    STUN = "stun"
    MANA_DRAIN = "mana_drain"
