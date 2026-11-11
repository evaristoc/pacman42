import pygame
from typing import Any, TypeAlias, TYPE_CHECKING
from src.PacMan.validation_contracts.event_enums import (
                                        IEventEnums,
                                        InGameEvents,
                                        MainMenuEvents,
                                        PauseMenuEvents)
if TYPE_CHECKING:
    from src.PacMan.renderer.assets import (
                                        ImgsAsset
    )

EventMsg: TypeAlias = dict[IEventEnums, dict[str, Any] | None] | None


EVENT_REGISTRY: dict[str, type[IEventEnums]] = {
    "START": MainMenuEvents,
    "CONTINUE": PauseMenuEvents,
    "CONTINUE": PauseMenuEvents,
}


def pacman_eh(
        self: "ImgsAsset",
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
        if event.key == pygame.K_c:
            msgs[InGameEvents.LEVEL_SKIP] = None
        else:
            None


def mainmenu_eh(
        self: "ImgsAsset",
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
                        raise SystemExit(0)
                    msgs[getattr(EVENT_REGISTRY[sk.event_name],
                                 sk.event_name)] = None
                    break


def pausemenu_eh(
        self: "ImgsAsset",
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
                        raise SystemExit(0)
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
