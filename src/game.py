from db import db
from classes.player import Player


class Game:
    def __init__(self, username: str) -> None:
        self.username = username.lower()
        self.player = Player(username)
