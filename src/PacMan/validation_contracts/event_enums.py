from enum import Enum, auto


class IEventEnums(Enum):
    pass


class MainMenuEvents(IEventEnums):
    START = auto()
    SETTINGS = auto()
    HIGHSCORES = auto()
    QUIT = auto()


class PauseMenuEvents(IEventEnums):
    CONTINUE = auto()
    QUIT = auto()


class InGameEvents(IEventEnums):
    PACMAN_NORTH = auto()
    PACMAN_EAST = auto()
    PACMAN_SOUTH = auto()
    PACMAN_WEST = auto()
    PAUSE = auto()


class HighScoreMenuEvents(IEventEnums):
    REGISTER = auto()
    CANCEL = auto()
