from dataclasses import dataclass

import config
from classes.enums import MoveType
from classes.stats import Stats


@dataclass
class Poison:
    duration: int
    multiplier: float


class PlayerSkill:
    def __init__(self, stats: Stats) -> None:
        self._stats = stats
        self._moves = [MoveType.ATTACK, ]

    def serialize(self) -> dict:
        return {
            "moves": [i.value for i in self._moves]
        }

    def grant(self, move: MoveType) -> None:
        """Grant a move.

        Args:
            move (MoveType): game.enums.MoveType
        """
        if move not in self._moves:
            self._moves.append(move)

    def get_all(self) -> list[MoveType]:
        """Get all avaliable moves.

        Returns:
            list[MoveType]: List of all avaliable moves.
        """
        return self._moves

    def can_use(self, move: MoveType) -> bool:
        """Can make this move?

        Args:
            move (MoveType): game.enums.MoveType

        Returns:
            bool: Yes or AAH.
        """
        return (
            self._stats.get("mana") >= config.PLAYER_MOVE_COSTS[move.value]
            and move in self._moves
        )
