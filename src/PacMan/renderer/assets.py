from collections import deque
from pathlib import Path
import pygame
from pygame.event import Event
from typing import Any
from src.PacMan.validation_contracts.event_enums import (
    InGameEvents,
    MainMenuEvents,
    HighScoreMenuEvents,
    HighScoreRegisterEvents,
    PauseMenuEvents
)
from src.PacMan.game_logic.gamemanager.game_sm import (
                            InGameState,
                            MainMenuState,
                            HighScoreMenuState,
                            HighScoreRegisterState,
                            PauseMenuState)
from src.PacMan.game_logic.ingame.characters.ghosts.ghosts import GhostName


ASSETS: dict[str, Any] = {
    InGameState.__name__: {
        # "events": {
        #         InGameEvents.PACMAN_WEST: pygame.K_RIGHT,
        #         InGameEvents.PACMAN_NORTH: pygame.K_UP,
        #         InGameEvents.PACMAN_EAST: pygame.K_LEFT,
        #         InGameEvents.PACMAN_SOUTH: pygame.K_DOWN,
        #         PauseMenuState: pygame.K_SPACE
        # },
        "assets": {
            "board": {
                "img": None,
                # "metadata": {
                #     "size_game": 1.0,
                # }
            },
            "pacman": {
                InGameEvents.PACMAN_EAST.name: deque([]),
                InGameEvents.PACMAN_NORTH.name: deque([]),
                InGameEvents.PACMAN_SOUTH.name: deque([]),
                InGameEvents.PACMAN_WEST.name: deque([]),
                "metadata": {
                    "resize_w_prop": 1.0,
                    "resize_h_prop": 1.0,
                }
            },
            "ghosts": {
                GhostName.BLINKY: None,
                GhostName.CLYDE: None,
                GhostName.INKY: None,
                GhostName.PINKY: None,
                "metadata": {
                    "resize_w_prop": 1.0,
                    "resize_h_prop": 1.0,
                }
            },
            "HUB_TOP": {
                "img": None,
                "text": "",
                "metadata": {
                    "text_x_prop": 1.0,
                    "text_y_prop": 1.0,
                    "font_size_prop": 1.0 / 20.8
                }
            },
            "HUB_BOTTOM": {
                "img": None,
                "text": "",
                "metadata": {
                    "text_x_prop": 1.0,
                    "text_y_prop": 1.0,
                    "font_size_prop": 1.0 / 20.8,
                    "lives_x": 1.0,
                    "lives_y": 1.0,
                    "lives_padding": 1.0
                },
            }
        }
    },
    MainMenuState.__name__: {
        # "events": {

        # },
        "assets": {
            MainMenuEvents.START.name: None,
            MainMenuEvents.HIGHSCORES.name: None,
            MainMenuEvents.INSTRUCTIONS.name: None,
            MainMenuEvents.EXIT.name: None,
            "metadata": {
                "resize_w_prop": 1 / 5,
                "resize_h_prop": 1 / 8,
                "x_pos_prop": 1.0,
                "y_pos_prop": 1.0,
                "gap": 1.0
            }
        }
    },
    PauseMenuState.__name__: {
        # "events": {

        # },
        "assets": {
            PauseMenuEvents.CONTINUE.name: None,
            PauseMenuEvents.EXIT.name: None,
            "metadata": {
                "resize_w_prop": 1 / 5,
                "resize_h_prop": 1 / 8,
                "x_pos_prop": 1.0,
                "y_pos_prop": 1.0,
                "gap": 1.0
            }
        }
    },
    HighScoreRegisterState.__name__: {
        # "events": {
        #     MainMenuState: HighScoreRegisterEvents.CANCEL
        # },
        "assets": {
            HighScoreRegisterEvents.REGISTER.name: None,
            HighScoreRegisterEvents.CANCEL.name: None,
            "metadata": {
                "resize_w_prop": 1 / 5,
                "resize_h_prop": 1 / 8,
                "x_pos_prop": 1.0,
                "y_pos_prop": 1.0,
                "gap": 1.0
            }
        }
    },
    HighScoreMenuState.__name__: {
        # "events": {},
        "assets": {
            HighScoreMenuEvents.RETURN.name: None,
            "medatadata": {
                "resize_w_prop": 1 / 5,
                "resize_h_prop": 1 / 8,
                "x_pos_prop": 1.0,
                "y_pos_prop": 1.0,
                "gap": 1.0
            }
        }
    },
    "GameOverState": {
        "assets": {
            "GameOverEvent": None,
            "metadata": {
                "resize_w_prop": 1 / 5,
                "resize_h_prop": 1 / 8,
                "x_pos_prop": 1.0,
                "y_pos_prop": 1.0,
                "gap": 1.0
            }
        }
    },
    "WiningState": {
        "assets": {
            "WinEvent": None,
            "metadata": {
                "resize_w_prop": 1 / 5,
                "resize_h_prop": 1 / 8,
                "x_pos_prop": 1.0,
                "y_pos_prop": 1.0,
                "gap": 1.0
            }
        }
    },
}