from typing import Optional

from classes import enums, errors
from classes.monsters import Monster, Monsters
from classes.player import Player
from classes.playerdata import PlayerData


class Game:
    """Game state per player.
    """

    def __init__(self, username: str) -> None:
        self.username = username.lower()
        self.player = Player(self.username)
        self.__pdata = PlayerData(self.username)
        # To call monster:
        # monster = game.monster.get("slime", damage=2, hp=20, mana=10).set_name("Your weird name")
        self.monsters = Monsters()
        self.monster: Optional[Monster] = None
        self.errors = errors
        self.enums = enums

    def get_monster(self, monster: str):
        monster_obj = self.monsters.get(monster)
        self.monster = monster_obj
        return monster_obj

    def save(self) -> None:
        """Save game.
        """
        self.__pdata["player"] = self.player.serialize()

        serialized = None
        if self.monster:
            serialized = self.monster.serialize()
        self.__pdata["monster"] = serialized

        self.__pdata.save()
