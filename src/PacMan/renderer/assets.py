from collections import deque
from pathlib import Path
import pygame
from pygame.event import Event
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable
from src.PacMan.validation_contracts.event_enums import (
    InGameEvents,
    MainMenuEvents,
    HighScoreMenuEvents,
    HighScoreRegisterEvents,
    PauseMenuEvents
)
from src.PacMan.renderer.renderer_engine import(
                            PyGMLXImageEmulator,
                            PyMLXPNGEmulator,
                            PyGMLXTextEmulator
)
from src.PacMan.game_logic.gamemanager.game_sm import (
                            InGameState,
                            MainMenuState,
                            HighScoreMenuState,
                            HighScoreRegisterState,
                            PauseMenuState)
from src.PacMan.game_logic.ingame.characters.ghosts.ghosts import GhostName


# class Loader(ABC):
#     @abstractmethod
#     def loader(self) -> None:
#         ...

@dataclass
class ImgMetadata:
    x_pos_prop:  float | None = field(default=None)
    y_pos_prop:  float | None = field(default=None)
    resize_w_prop: float | None = field(default=None)
    resize_h_prop: float | None = field(default=None)
    gap_x_prop:  float | None = field(default=None)
    gap_y_prop:  float | None = field(default=None)

    # img_metadata: ImgMetadata = field(default_factory=ImgMetadata)

@dataclass
class TextMetadata(ImgMetadata):
    text: str = field(default='')
    text_x_prop: float | None = field(default=None)
    text_y_prop: float | None = field(default=None)
    font_size_prop: float = field(default=1.0 / 20.8)


# @dataclass(frozen=False)
# class LivesMetadata(ImgMetadata):

@dataclass
class Source:
    event_name: str = field(default='')
    path: Path = field(default_factory=Path)
    img: (PyGMLXTextEmulator | PyMLXPNGEmulator | PyGMLXImageEmulator) = field(default_factory=PyGMLXImageEmulator)
    metadata: (ImgMetadata | TextMetadata) = field(default_factory=ImgMetadata)

@dataclass
class ImgsAsset:
    asset_name: str = field(default='')
    sources: dict[str, Source | deque[Source]] = field(default_factory=dict)


@dataclass
class Assets:
    state_name: str = field(default='')
    img_assets: dict[str, ImgsAsset] = field(default_factory=dict)


@dataclass
class Events:
    state_name: str = field(default='')
    events: dict[str, pygame.Event | Callable] = field(default_factory=dict)


@dataclass
class AssetMap:
    events = field(default_factory=Events)
    assets = field(default_factory=Assets)


@dataclass
class AssetRegistry:
    InGameState.__name__ = field(default_factory=AssetMap)
    MainMenuState.__name__ = field(default_factory=AssetMap)
    PauseMenuState.__name__ = field(default_factory=AssetMap)
    HighScoreMenuState.__name__ = field(default_factory=AssetMap)
    HighScoreRegisterState.__name__ = field(default_factory=AssetMap)


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
                    "lives_x_prop": 1.0,
                    "lives_y_prop": 1.0,
                    "lives_padding_prop": 1.0
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
                "gap_x": 1.0,
                "gap_y": 1.0
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