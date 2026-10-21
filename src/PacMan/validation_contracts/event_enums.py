from enum import Enum, auto


class MainMenuEvents(Enum):
    START = auto()
    SETTINGS = auto()
    HIGHSCORES = auto()
    QUIT = auto()


class PauseMenuEvents(Enum):
    CONTINUE = auto()
    QUIT = auto()


class InGameEvents(Enum):
    PACMAN_NORTH = auto()
    PACMAN_EAST = auto()
    PACMAN_SOUTH = auto()
    PACMAN_WEST = auto()
    PAUSE = auto()


class HighScoreMenuEvents(Enum):
    REGISTER = auto()
    CANCEL = auto()
