import pygame
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


EVENT_REGISTRY: dict[str, type[IEventEnums]] = {
    "main": MainMenuEvents,
    "pause": PauseMenuEvents
}


def pacman_eh(
        self: ImgsAsset,
        event: pygame.event.Event,
        msgs: EventMsg) -> None:
    _ = self
    if msgs is None:
        return
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


def menuwithexit_eh(
        self: ImgsAsset,
        event: pygame.event.Event,
        msgs: EventMsg) -> None:
    if msgs is None:
        return
    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos
        buttons = list(self.sources.keys())
        for b_ in buttons:
            sk = self.get_source(b_)
            if (sk.metadata.x_pos_prop is not None
                    and sk.metadata.y_pos_prop is not None):
                start_x = sk.metadata.x_pos_prop
                start_y = sk.metadata.y_pos_prop
                if sk.img.contains(x,
                                   y,
                                   start_x,
                                   start_y):
                    if sk.event_name == 'EXIT':
                        SystemExit(0)
                    msgs[getattr(EVENT_REGISTRY[sk.event_name],
                                 sk.event_name)] = None
                    break


# def pausemenu_eh(
#         self: ImgsAsset,
#         event: pygame.event.Event,
#         msgs: EventMsg) -> None:
#     if msgs is None:
#         return
#     if event.type == pygame.MOUSEBUTTONDOWN:
#         x, y = event.pos
#         if self.get_source('CONTINUE').img.contains(x, y):
#             msgs[PauseMenuEvents.CONTINUE] = None
#         if self.get_source('EXIT').img.contains(x, y):
#             SystemExit(0)
#         else:
#             None
