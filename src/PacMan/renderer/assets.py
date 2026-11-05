import deque
import pygame
from pygame.event import Event
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

ASSETS = {
    InGameState: {
        "events": {
                InGameEvents.PACMAN_WEST: pygame.K_RIGHT,
                InGameEvents.PACMAN_NORTH: pygame.K_UP,
                InGameEvents.PACMAN_EAST: pygame.K_LEFT,
                InGameEvents.PACMAN_SOUTH: pygame.K_DOWN,
                PauseMenuState: pygame.K_SPACE
        },
        "assets": {
            "pacman": {
                InGameEvents.PACMAN_EAST: deque([]),
                InGameEvents.PACMAN_NORTH: deque([]),
                InGameEvents.PACMAN_SOUTH: deque([]),
                InGameEvents.PACMAN_WEST: deque([]),
                "metadata": {
                    "resize_prop": 1.0
                }
            },
            "ghosts": {
                GhostName.BLINKY: None,
                GhostName.CLYDE: None,
                GhostName.INKY: None,
                GhostName.PINKY: None,
                "metadata": {
                    "resize_prop": 1.0
                }
            },
            "HUB_TOP": {
                "img": None,
                "text": "",
                "metadata": {
                    "text_x_prop": 1.0,
                    "text_y_prop": 1.0,
                    "font_size_prop": 1.0
                }
            },
            "HUB_BOTTOM": {
                "img": None,
                "text": "",
                "metadata": {
                    "text_x_prop": 1.0,
                    "text_y_prop": 1.0,
                    "font_size_prop": 1.0,
                    "lives_x": 1.0,
                    "lives_y": 1.0,
                    "lives_padding": 1.0
                },
            }
        }
    },
    MainMenuState: {
        "events": {

        },
        "assets": {
            MainMenuEvents.START: None,
            MainMenuEvents.HIGHSCORES: None,
            MainMenuEvents.INSTRUCTIONS: None,
            MainMenuEvents.EXIT: None,
            "metadata": {
                "resize_prop": 1.0
            }
        }
    },
    PauseMenuState: {
        "events": {

        },
        "assets": {
            PauseMenuEvents.CONTINUE: None,
            PauseMenuEvents.EXIT: None,
            "metadata": {}
        }
    },
    HighScoreRegisterState: {
        "events": {
            MainMenuState: HighScoreRegisterEvents.CANCEL
        },
        "assets": {
            HighScoreRegisterEvents.REGISTER: None,
            HighScoreRegisterEvents.CANCEL: None,
            "metadata": {
                "resize_prop": 1.0
            }
        }
    },
    HighScoreMenuState: {
        "events": {},
        "assets": {
            HighScoreMenuEvents.RETURN: None,
        }
    }
}