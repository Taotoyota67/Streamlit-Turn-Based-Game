# from db import db # Not used, yet
from classes.player import Player
from classes.monsters import Monsters


class Game:
    """Game state per player.
    """

    def __init__(self, username: str) -> None:
        self.username = username.lower()
        self.player = Player(self.username)
        # To call monster:
        # monster = game.monster.get("slime", damage=2, hp=20, mana=10).set_name("Your weird name")
        self.monsters = Monsters()

    def save(self) -> None:
        """Save game.
        """
        self.player.save()
