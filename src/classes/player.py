
import config
from classes.entity import Entity
from classes.enums import MoveType
from classes.errors import CannotMakeMove
from classes.playerdata import PlayerData
from classes.skills import PlayerSkill
from classes.stats import Stats


class Player:
    def __init__(self, username: str) -> None:
        self.username = username
        self._pdata = PlayerData(username)
        self.stats = Stats(**config.PLAYER_DEFAULT_STATS)
        self.entity = Entity(stats=self.stats)
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
            bool: Yay or Nay
        """
        return self.entity.is_poison()

    def is_stun(self) -> bool:
        """Is player entity stunned?

        Returns:
            bool: Yes or no
        """
        return self.entity.is_stun()

    def make_move(self, move: MoveType, target: Entity) -> int:
        """Make a move

        Args:
            move (MoveType): enums from game.enums.MoveType
            target (Entity): target of the move. (if heal, put player.entity)

        Returns:
            int: amount of damage or amount of heal, could be 1 for poison and etc.
        """
        if not self.skills.can_use(move):
            raise CannotMakeMove

        return self.entity.make_move(move, target)

    def save(self) -> None:
        """Save player.
        """
        self._pdata["playerStats"] = self.stats.serialize()
        self._pdata["playerCombat"] = self.entity.serialize()

        self._pdata.save()
