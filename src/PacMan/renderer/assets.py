import logging
from collections import deque
from pathlib import Path
import pygame
from dataclasses import dataclass, field
from typing import Callable, TypeAlias
from src.PacMan.renderer.renderer_engine import (
                            PyGMLXImageEmulator,
                            PyMLXPNGEmulator,
                            PyGMLXTextEmulator
)
from src.PacMan.renderer.event_handlers import EventMsg

logger = logging.getLogger(__name__)


@dataclass
class ImgMetadata:
    x_pos_prop:  int | None = field(default=None)
    y_pos_prop:  int | None = field(default=None)
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
    text_x_prop: int | None = field(default=None)
    text_y_prop: int | None = field(default=None)
    font_size_prop: float = field(default=1.0 / 20.8)
    font_path: str = field(default="CONSOLA.TTF")
    color: int = field(default=0xF6303F)

    def create_text(self,
                    **values: str | int | float) -> None:
        self.text = self.text_template.format(**values)


@dataclass
class Source:
    img: (PyGMLXTextEmulator
          | PyMLXPNGEmulator
          | PyGMLXImageEmulator)
    event_name: str = field(default='')
    type: str = field(default='runtime')
    path: Path = field(default_factory=Path)
    metadata: (ImgMetadata | TextMetadata) = field(default_factory=ImgMetadata)


Sources: TypeAlias = Source | deque[Source]


@dataclass
class ImgsAsset:
    asset_name: str = field(default='')
    sources: dict[str, Sources] = field(default_factory=dict)
    event_handler: Callable[[pygame.event.Event, EventMsg], None] | None = None

    def get_source(self, event_name: str) -> Source:
        source = self.sources[event_name]
        if not isinstance(source, Source):
            logger.error(f"Returning wrong source type - {event_name}")
            raise SystemExit(1)
        return source

    def get_animation(
        self,
        event_name: str,
    ) -> deque[Source]:
        source = self.sources[event_name]
        if not isinstance(source, deque):
            logger.error(f"Returning wrong source type - {event_name}")
            raise SystemExit(1)
        return source


@dataclass
class Assets:
    state_name: str = field(default='')
    img_assets: dict[str, ImgsAsset] = field(default_factory=dict)


@dataclass
class AssetRegistry:
    init: Assets = field(default_factory=Assets)
    ingamestate: Assets = field(default_factory=Assets)
    mainmenustate: Assets = field(default_factory=Assets)
    pausemenustate: Assets = field(default_factory=Assets)
    highscoremenustate: Assets = field(default_factory=Assets)
    highscoreregisterstate: Assets = field(default_factory=Assets)
