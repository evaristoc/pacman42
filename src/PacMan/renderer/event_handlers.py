import pygame
from pygame import Event
from typing import Any, TypeAlias
from src.PacMan.validation_contracts.event_enums import (
                                        IEventEnums,
                                        InGameEvents,
                                        MainMenuEvents,
                                        PauseMenuEvents)
from src.PacMan.renderer.assets import (
                                    ImgsAsset
)

EventMsg: TypeAlias = dict[IEventEnums, dict[str, Any] | None] | None


def pacman_eh(
        self,
        event: Event,
        msgs: EventMsg) -> None:
    _ = self
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_DOWN:
            msgs[InGameEvents.PACMAN_SOUTH] = None
        if event.key == pygame.K_UP:
            msgs[InGameEvents.PACMAN_NORTH] = None
        if event.key == pygame.K_LEFT:
            msgs[InGameEvents.PACMAN_WEST] = None
        if event.key == pygame.K_RIGHT:
            msgs[InGameEvents.PACMAN_EAST] = None
        if event.key == pygame.K_SPACE:
            msgs[InGameEvents.PAUSE] = None
        else:
            None


def mainmenu_eh(
        self,
        event: Event,
        msgs: EventMsg) -> None:
    if event.type == pygame.MOUSEBUTTONDOWN:
        imgassets: ImgsAsset = self.img_assets
        x, y = event.pos
        for i, sk in enumerate(imgassets['main'].sources.keys()):
            start_x = imgassets['main'].sources[sk].metadata.x_pos_prop
            start_y = imgassets['main'].sources[sk].metadata.y_pos_prop
            if imgassets['main'].sources[sk].img.contains(x, y, start_x, start_y):
                if sk == 'EXIT':
                    SystemExit(0)
                msgs[getattr(MainMenuEvents, sk)] = None
                break


def pausemenu_eh(
        self,
        event: Event,
        msgs: EventMsg) -> None:
    if event.type == pygame.MOUSEBUTTONDOWN:
        imgassets = self.img_assets
        x, y = event.pos
        if imgassets.sources['CONTINUE'].img.contains(x, y):
            msgs[PauseMenuEvents.CONTINUE] = None
        if imgassets.sources['EXIT'].img.contains(x, y):
            SystemExit(0)
        else:
            None
