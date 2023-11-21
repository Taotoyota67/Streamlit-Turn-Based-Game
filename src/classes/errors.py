
class GameException(Exception):
    """Base game exception"""


class InvalidMove(GameException):
    """Invalid move"""


class CannotMakeMove(GameException):
    """Lack of mana or move has not been granted"""


class CannotMove(GameException):
    """Cannot make the move, maybe due to stun or entity is dead"""


class AlreadyDead(GameException):
    """This entity is already dead and cannot do anything"""
