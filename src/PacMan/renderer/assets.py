from collections import deque
from pathlib import Path
import pygame
from dataclasses import dataclass, field
from typing import Callable
from src.PacMan.validation_contracts.event_enums import IEventEnums
from src.PacMan.renderer.renderer_engine import (
                            PyGMLXImageEmulator,
                            PyMLXPNGEmulator,
                            PyGMLXTextEmulator
)


@dataclass
class ImgMetadata:
    x_pos_prop:  float | None = field(default=None)
    y_pos_prop:  float | None = field(default=None)
    resize_w_prop: float | None = field(default=None)
    resize_h_prop: float | None = field(default=None)
    gap_x_prop:  float | None = field(default=None)
    gap_y_prop:  float | None = field(default=None)
    size_vp_w: int | None = field(default=None)
    size_vp_h: int | None = field(default=None)
    bg_color: int | None = field(default=0x00000000)


@dataclass
class TextMetadata(ImgMetadata):
    text: str = field(default='')
    text_template: str = field(default='')
    text_x_prop: float | None = field(default=None)
    text_y_prop: float | None = field(default=None)
    font_size_prop: float = field(default=1.0 / 20.8)
    font_path: str = field(default="CONSOLA.TTF")
    color: int = field(default=0xF6303F)

    def create_text(self,
                    **values: str | int | float) -> None:
        self.text = self.text_template.format(**values)

@dataclass
class Source:
    event_name: str = field(default='')
    type: str = field(default='runtime')
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
    event_handler: Callable[[pygame.event.Event], None] | None = None

    # def eventmap(
    #         self,
    #         e: pygame.event.Event,
    #         cb: Callable[[pygame.event.Event], IEventEnums]) -> IEventEnums:
    #     ...


# @dataclass
# class EventMap:
#     state_name: str = field(default='')
#     eventmapfunc: Callable[[pygame.Event], IEventEnums] | None = None


# @dataclass
# class AssetComp:
#     eventmap = field(default_factory=EventMap)
#     assets = field(default_factory=Assets)


@dataclass
class AssetRegistry:
    init: Assets = field(default_factory=Assets)
    ingamestate: Assets = field(default_factory=Assets)
    mainmenustate: Assets = field(default_factory=Assets)
    pausemenustate: Assets = field(default_factory=Assets)
    highscoremenustate: Assets = field(default_factory=Assets)
    highscoreregisterstate: Assets = field(default_factory=Assets)


# ASSETS: dict[str, Any] = {
#     InGameState.__name__: {
#         # "events": {
#         #         InGameEvents.PACMAN_WEST: pygame.K_RIGHT,
#         #         InGameEvents.PACMAN_NORTH: pygame.K_UP,
#         #         InGameEvents.PACMAN_EAST: pygame.K_LEFT,
#         #         InGameEvents.PACMAN_SOUTH: pygame.K_DOWN,
#         #         PauseMenuState: pygame.K_SPACE
#         # },
#         "assets": {
#             "board": {
#                 "img": None,
#                 # "metadata": {
#                 #     "size_game": 1.0,
#                 # }
#             },
#             "pacman": {
#                 InGameEvents.PACMAN_EAST.name: deque([]),
#                 InGameEvents.PACMAN_NORTH.name: deque([]),
#                 InGameEvents.PACMAN_SOUTH.name: deque([]),
#                 InGameEvents.PACMAN_WEST.name: deque([]),
#                 "metadata": {
#                     "resize_w_prop": 1.0,
#                     "resize_h_prop": 1.0,
#                 }
#             },
#             "ghosts": {
#                 GhostName.BLINKY: None,
#                 GhostName.CLYDE: None,
#                 GhostName.INKY: None,
#                 GhostName.PINKY: None,
#                 "metadata": {
#                     "resize_w_prop": 1.0,
#                     "resize_h_prop": 1.0,
#                 }
#             },
#             "HUB_TOP": {
#                 "img": None,
#                 "text": "",
#                 "metadata": {
#                     "text_x_prop": 1.0,
#                     "text_y_prop": 1.0,
#                     "font_size_prop": 1.0 / 20.8
#                 }
#             },
#             "HUB_BOTTOM": {
#                 "img": None,
#                 "text": "",
#                 "metadata": {
#                     "text_x_prop": 1.0,
#                     "text_y_prop": 1.0,
#                     "font_size_prop": 1.0 / 20.8,
#                     "lives_x_prop": 1.0,
#                     "lives_y_prop": 1.0,
#                     "lives_padding_prop": 1.0
#                 },
#             }
#         }
#     },
#     MainMenuState.__name__: {
#         # "events": {

#         # },
#         "assets": {
#             MainMenuEvents.START.name: None,
#             MainMenuEvents.HIGHSCORES.name: None,
#             MainMenuEvents.INSTRUCTIONS.name: None,
#             MainMenuEvents.EXIT.name: None,
#             "metadata": {
#                 "resize_w_prop": 1 / 5,
#                 "resize_h_prop": 1 / 8,
#                 "x_pos_prop": 1.0,
#                 "y_pos_prop": 1.0,
#                 "gap_x": 1.0,
#                 "gap_y": 1.0
#             }
#         }
#     },
#     PauseMenuState.__name__: {
#         # "events": {

#         # },
#         "assets": {
#             PauseMenuEvents.CONTINUE.name: None,
#             PauseMenuEvents.EXIT.name: None,
#             "metadata": {
#                 "resize_w_prop": 1 / 5,
#                 "resize_h_prop": 1 / 8,
#                 "x_pos_prop": 1.0,
#                 "y_pos_prop": 1.0,
#                 "gap": 1.0
#             }
#         }
#     },
#     HighScoreRegisterState.__name__: {
#         # "events": {
#         #     MainMenuState: HighScoreRegisterEvents.CANCEL
#         # },
#         "assets": {
#             HighScoreRegisterEvents.REGISTER.name: None,
#             HighScoreRegisterEvents.CANCEL.name: None,
#             "metadata": {
#                 "resize_w_prop": 1 / 5,
#                 "resize_h_prop": 1 / 8,
#                 "x_pos_prop": 1.0,
#                 "y_pos_prop": 1.0,
#                 "gap": 1.0
#             }
#         }
#     },
#     HighScoreMenuState.__name__: {
#         # "events": {},
#         "assets": {
#             HighScoreMenuEvents.RETURN.name: None,
#             "medatadata": {
#                 "resize_w_prop": 1 / 5,
#                 "resize_h_prop": 1 / 8,
#                 "x_pos_prop": 1.0,
#                 "y_pos_prop": 1.0,
#                 "gap": 1.0
#             }
#         }
#     },
#     "GameOverState": {
#         "assets": {
#             "GameOverEvent": None,
#             "metadata": {
#                 "resize_w_prop": 1 / 5,
#                 "resize_h_prop": 1 / 8,
#                 "x_pos_prop": 1.0,
#                 "y_pos_prop": 1.0,
#                 "gap": 1.0
#             }
#         }
#     },
#     "WiningState": {
#         "assets": {
#             "WinEvent": None,
#             "metadata": {
#                 "resize_w_prop": 1 / 5,
#                 "resize_h_prop": 1 / 8,
#                 "x_pos_prop": 1.0,
#                 "y_pos_prop": 1.0,
#                 "gap": 1.0
#             }
#         }
#     },
# }