
class GameException(Exception):
    """Base game exception"""


class InvalidMove(GameException):
    """Invalid move"""


class CannotMakeMove(GameException):
    """Cannot make the move, maybe due to stun or entity is dead"""
