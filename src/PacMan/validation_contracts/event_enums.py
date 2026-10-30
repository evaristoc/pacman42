from enum import Enum, auto


class IEventEnums(Enum):
    pass


class MainMenuEvents(IEventEnums):
    START = auto()
    CHEATING = auto()
    HIGHSCORES = auto()
    QUIT = auto()


class CheatingMenuEvents(IEventEnums):
    IMPOTENTGHOSTS = auto()
    RETURN = auto()


class HighScoreMenuEvents(IEventEnums):
    RETURN = auto()


class PauseMenuEvents(IEventEnums):
    CONTINUE = auto()
    QUIT = auto()


class InGameEvents(IEventEnums):
    PACMAN_NORTH = auto()
    PACMAN_EAST = auto()
    PACMAN_SOUTH = auto()
    PACMAN_WEST = auto()
    PAUSE = auto()


class HighScoreRegisterEvents(IEventEnums):
    REGISTER = auto()
    CANCEL = auto()
