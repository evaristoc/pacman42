from enum import Enum, auto


class MainMenuButtons(Enum):
    START = auto()
    SETTINGS = auto()
    HIGHSCORES = auto()
    QUIT = auto()


class PauseMenuButtons(Enum):
    CONTINUE = auto()
    QUIT = auto()
