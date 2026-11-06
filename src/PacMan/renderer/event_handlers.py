import pygame
from pygame import Event
from typing import Any, TypeAlias
from src.PacMan.validation_contracts.event_enums import (
                                        IEventEnums,
                                        InGameEvents,
                                        MainMenuEvents,
                                        PauseMenuEvents)

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
    return msgs


def mainmenu_eh(
        self,
        event: Event,
        msgs: EventMsg) -> None:
    if event.type == pygame.MOUSEBUTTONDOWN:
        imgassets = self.img_assets
        x, y = event.pos
        if imgassets.sources['START'].img.contains(x, y):
            msgs[MainMenuEvents.START] = None
        if imgassets.sources['INSTRUCTIONS'].img.contains(x, y):
            msgs[MainMenuEvents.INSTRUCTIONS] = None
        if imgassets.sources['HIGHSCORES'].img.contains(x, y):
            msgs[MainMenuEvents.HIGHSCORES] = None
        if imgassets.sources['EXIT'].img.contains(x, y):
            SystemExit(0)
        else:
            None
    return msgs


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
    return msgs
