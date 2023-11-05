from .playerdata import PlayerData


class Player:
    def __init__(self, username: str) -> None:
        self._username = username
        self._pdata = PlayerData(username)


# game.monster.spawn(game.entity.Slime)
# game.player.startCombat()
# player.stats
# player.combat
# game.player.
