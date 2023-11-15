import config
from classes.entity import Entity
from classes.enums import MoveType
from classes.errors import CannotMakeMove
from classes.skills import PlayerSkill
from classes.stats import Stats


class Player:
    def __init__(self, username: str) -> None:
        self.username = username
        self.stats = Stats(**config.PLAYER_DEFAULT_STATS)
        self.entity = Entity(stats=self.stats, is_player=True)
        self.skills = PlayerSkill(self.stats)

    def tick(self) -> None:
        """Tick, Call this at the start of the turn.
        """
        return self.entity.tick()

    def is_alive(self) -> bool:
        """Is player entity alive?

        Returns:
            bool: Yes or naa?
        """
        return self.entity.is_alive()

    def is_poison(self) -> bool:
        """Is player entity poisoned?

        Returns:
            bool: Yay or Nay.
        """
        return self.entity.is_poison()

    def is_stun(self) -> bool:
        """Is player entity stunned?

        Returns:
            bool: Yes or no.
        """
        return self.entity.is_stun()

    def make_move(self, move: MoveType, target: Entity) -> int:
        """Make a move.

        Args:
            move (MoveType): Enums from game.enums.MoveType
            target (Entity): target of the move. (if heal, put player.entity or monster.)

        Returns:
            int: amount of damage or amount of heal, could be 1 for poison and etc.
        """
        if not self.skills.can_use(move):
            raise CannotMakeMove(
                "Cannot make a move due to mana or skill not granted."
            )

        mana_cost = config.PLAYER_MOVE_COSTS[move.value]
        self.stats.mana.reduce(mana_cost, 0)

        return self.entity.make_move(move, target)

    def serialize(self) -> dict:
        return {
            "entity": self.entity.serialize(),
            "skills": self.skills.serialize()
        }
