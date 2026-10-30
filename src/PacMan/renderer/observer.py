from __future__ import annotations
import pygame
from pygame import Event
from typing import TypeVar, Type, Any, Protocol, TypeAlias, TYPE_CHECKING
from src.PacMan.validation_contracts.event_enums import (
                                        IEventEnums,
                                        InGameEvents)
from src.PacMan.game_logic.gamemanager.gamelogicmng import GameLogicManager
from src.PacMan.game_logic.gamemanager.game_sm import (
                                                IGameState,
                                                InGameState)
if TYPE_CHECKING:  # only required for parameter type assignment 
    from src.PacMan.renderer.drawer_engine import DrawerEngine
    from src.PacMan.renderer.renderer_engine import PyGMiniLibXEmulator

T = TypeVar("T", bound="IAction")
EventMsg: TypeAlias = dict[IEventEnums, dict[str, Any] | None] | None


class IAction(Protocol):
    def action(
            self,
            obs: "Observer"
            ) -> None:
        ...


# class PlayingActionPacman:
#     def action(
#             self,
#             obs: "Observer"
#             ) -> None:
#         print(f"this is {self.__class__.__name__}")
#         print(obs._registry)
#         print(obs._glm.character_manager.pacman.position)
#         print(obs._glm.character_manager.ghost_mng.ghosts)
#         # # PACMAN ###
#         pm = obs._registry["pacman"]["moves"].pop()
#         obs._mlx.pygmlx_put_image_to_window(
#             pm,
#             obs._drawer.next_char_coord(obs._glm.character_manager.pacman.position[0]),
#             obs._drawer.next_char_coord(obs._glm.character_manager.pacman.position[1]) + obs._drawer.bottom_h
#         )
#         obs._registry["pacman"]["moves"].append(pm)  # ALWAYS

#         # # GHOSTS ###
#         # for g in obs._glm.character_manager.ghost_mng.ghosts:
#         #     obs._mlx.pygmlx_put_image_to_window(
#         #         obs._registry["ghosts"][g.name],
#         #         obs._drawer.next_char_coord(obs._glm.character_manager.ghost_mng.ghosts[g].position[0]),
#         #         obs._drawer.next_char_coord(obs._glm.character_manager.ghost_mng.ghosts[g].position[1]) + obs._drawer.bottom_h
#         #     )


# class PlayingActionGhosts:
#     def action(
#             self,
#             obs: "Observer"
#             ) -> None:
#         # GHOSTS ###
#         for g in obs._glm.character_manager.ghost_mng.ghosts:
#             obs._mlx.pygmlx_put_image_to_window(
#                 obs._registry["ghosts"][g.name],
#                 obs._drawer.next_char_coord(obs._glm.character_manager.ghost_mng.ghosts[g].position[0]),
#                 obs._drawer.next_char_coord(obs._glm.character_manager.ghost_mng.ghosts[g].position[1]) + obs._drawer.bottom_h
#             )


# class PlayingActionBoard:
#     def action(
#             self,
#             obs: "Observer"
#             ) -> None:
#         # INTERIOR CELLS ###
#         # -- pacman --
#         obs._drawer.draw_cell_interior(
#             obs._registry["board"],
#             obs._glm.character_manager.pacman.old_position,
#             0x000
#         )
#         # -- ghosts --
#         for g in obs._glm.character_manager.ghost_mng.ghosts:
#             obs._drawer.draw_cell_interior(
#                 obs._registry["board"],
#                 obs._glm.character_manager.ghost_mng.ghosts[g].old_position,
#                 0x000
#             )
#         obs._mlx.pygmlx_put_image_to_window(
#             obs._registry["board"],
#             obs._drawer.margin / 2,
#             obs._drawer.margin / 2 + obs._drawer.bottom_h
#         )
#         # MENUS ###
#         # # -- hub --
#         # obs._mlx.pygmlx_put_image_to_window(
#         #     obs._registry["menus"]["hub"],
#         #     obs._drawer.margin / 2,
#         #     obs._drawer.margin / 2 + obs._mlx.height
#         # )

#         # for i, img in enumerate(obs._registry["menus"]["start"].keys()):
#         #     obs._mlx.pygmlx_put_image_to_window(
#         #         obs._registry["menus"]["start"][img],
#         #         int(obs._drawer.margin / 2) + 200,
#         #         int(obs._drawer.margin / 2) + obs._drawer.bottom_h + i * 100
#         #         ) 


class PlayingAction(IAction):
    def action(
            self,
            obs: Observer
    ) -> None:
        # INTERIOR CELLS ###
        # -- pacman --
        obs._drawer.draw_cell_interior(
            obs._registry["board"],
            obs._glm.character_manager.pacman.old_position,
            0x000
        )
        # -- ghosts --
        for g in obs._glm.character_manager.ghost_mng.ghosts:
            obs._drawer.draw_cell_interior(
                obs._registry["board"],
                obs._glm.character_manager.ghost_mng.ghosts[g].old_position,
                0x000
            )
        obs._mlx.pygmlx_put_image_to_window(
            obs._registry["board"],
            obs._drawer.margin / 2,
            obs._drawer.margin / 2 + obs._drawer.bottom_h
        )
        # MENUS ###
        # # -- hub --
        # obs._mlx.pygmlx_put_image_to_window(
        #     obs._registry["menus"]["hub"],
        #     obs._drawer.margin / 2,
        #     obs._drawer.margin / 2 + obs._mlx.height
        # )

        # # PACMAN ###
        pm = obs._registry["pacman"]["moves"].pop()
        print(pm)
        obs._mlx.pygmlx_put_image_to_window(
            pm,
            obs._drawer.next_char_coord(obs._glm.character_manager.pacman.position[0]),
            obs._drawer.next_char_coord(obs._glm.character_manager.pacman.position[1]) + obs._drawer.bottom_h
        )
        obs._registry["pacman"]["moves"].append(pm)  # ALWAYS

        # GHOSTS ###
        # for g in obs._glm.character_manager.ghost_mng.ghosts:
        #     obs._mlx.pygmlx_put_image_to_window(
        #         obs._registry["ghosts"][g.name],
        #         obs._drawer.next_char_coord(obs._glm.character_manager.ghost_mng.ghosts[g].position[0]),
        #         obs._drawer.next_char_coord(obs._glm.character_manager.ghost_mng.ghosts[g].position[1]) + obs._drawer.bottom_h
        #     )

        # for i, img in enumerate(obs._registry["menus"]["start"].keys()):
        #     obs._mlx.pygmlx_put_image_to_window(
        #         obs._registry["menus"]["start"][img],
        #         int(obs._drawer.margin / 2) + 200,
        #         int(obs._drawer.margin / 2) + obs._drawer.bottom_h + i * 100
        #         )         


HANDLER_REGISTRY: dict[Type[IGameState], Type[IAction]] = {
    InGameState: PlayingAction
}


class Observer:
    def __init__(self,
                 mlx: PyGMiniLibXEmulator,
                 glm: GameLogicManager,
                 drawer: "DrawerEngine") -> None:
        self._registry: dict[str, Any] | None = None
        self._mlx = mlx
        self._glm = glm
        self._drawer = drawer
        self.event_queue: list[Event] = []

    def register_assets(self, key: str, asset: dict[str, Any]) -> None:
        if not self._registry:
            self._registry = {}
        # print(asset)
        self._registry[key] = asset

    def _actions(self,
                 msgs: EventMsg | None) -> None:
        self._glm.update_logic(msgs)
        if isinstance(self._glm.state, IGameState):
            self.action = self._get_action(state=self._glm.state)().action(self)

    def state_loop(
            self
    ) -> bool:
        msgs: EventMsg = {}
        for event in self.event_queue:
            if event.type == pygame.QUIT:
                return False
            self._translate_events(event, msgs)
        self._actions(msgs)
        return True

    def _get_action(
            self,
            state: IGameState,
            ) -> Type[T]:
        return HANDLER_REGISTRY[type(state)]

    def _translate_events(self,
                          event: Event,
                          msgs: EventMsg
                          ) -> None:
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
