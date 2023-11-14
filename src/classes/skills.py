from dataclasses import dataclass

import config
from classes.enums import MoveType
from classes.stats import Stats


@dataclass
class Buff:
    duration: int
    multiplier: float


@dataclass
class Poison:
    duration: int
    multiplier: float


class PlayerSkill:
    def __init__(self, stats: Stats) -> None:
        self._stats = stats
        self._moves = [MoveType.ATTACK, ]

    def grant(self, move: MoveType) -> None:
        self._moves.append(move)

    def get_all(self) -> list[MoveType]:
        return self._moves

    def can_use(self, move: MoveType) -> bool:
        return (
            self._stats.get("mana") >= config.PLAYER_MOVE_COSTS[move.value]
            and move in self._moves
        )
