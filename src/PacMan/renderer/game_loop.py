from __future__ import annotations
import logging
import pygame
from pygame import Event
from typing import TypeVar, Type, Protocol, TYPE_CHECKING
from src.PacMan.game_logic.gamemanager.gamelogicmng import (
                                                    GameLogicManager,
                                                    GLMSnapshot)
from src.PacMan.game_logic.gamemanager.game_sm import (
                                                IGameState,
                                                MainMenuState,
                                                InGameState,
                                                GameOverPlayerLost)
if TYPE_CHECKING:  # only required for parameter type assignment
    from src.PacMan.renderer.drawer_engine import BoardDrawerEngine
    from src.PacMan.renderer.assets import ImgsAsset, Assets, AssetRegistry
    from src.PacMan.renderer.renderer_engine import PyGMiniLibXEmulator
    from src.PacMan.renderer.event_handlers import EventMsg
    from src.PacMan.renderer.renderer_assembler import RendererAssembler

logger = logging.getLogger(__name__)


T = TypeVar("T", bound="IAction")


class IAction(Protocol):
    def action(
            self,
            gloop: "GameLoop",
            tick: int
            ) -> None:
        ...

    def _init_state(
            self,
            gloop: "GameLoop"
    ) -> None:
        ...


class MainMenuAction(IAction):
    def action(
            self,
            gloop: GameLoop,
            tick: int
    ) -> None:
        _ = tick
        if gloop._statechanged:
            self._init_state(gloop)

    def _init_state(
            self,
            gloop: GameLoop
    ) -> None:
        try:
            background = gloop._mlx.pygmlx_new_image(
                gloop._mlx.view_w,
                gloop._mlx.view_h
            )
            gloop._mlx.pygmlx_put_image_to_window(
                background,
                0,
                0
            )
            buttons = list(gloop._registry.mainmenustate.img_assets['main']
                           .sources.keys())
            for button in buttons:
                b_ = gloop._registry.mainmenustate.img_assets['main']\
                    .get_source(button)
                if (b_.metadata and b_.metadata.x_pos_prop is not None
                        and b_.metadata.y_pos_prop is not None):
                    gloop._mlx.pygmlx_put_image_to_window(
                        b_.img,
                        b_.metadata.x_pos_prop,
                        b_.metadata.y_pos_prop
                    )
        except Exception as err:
            logger.error(f"FATAL: Exception trying to load menus: {err}")
            raise SystemExit(1)


class PlayingAction(IAction):
    # def _init_start(self,
    #                 gloop: GameLoop) -> None:
    def action(
            self,
            gloop: GameLoop,
            tick: int
    ) -> None:
        if gloop._levelchanged:
            self._get_newlevel(gloop)
        if gloop._statechanged:
            self._init_state(gloop)
        else:
            self._update_state(gloop, tick)

    def _get_newlevel(
            self,
            gloop: 'GameLoop'
    ) -> None:
        # # TODO update nb_cells config before drawer
        # # NOTE I need to compute before loading, need those values
        # self.drawer.compute(gloop._assembler._config)
        # gloop._drawer.basic_calcs()
        # nb_cells = self.glm.session.maze.nb_cells
        # self.assewmber._config = self.assewmber._config.model_copy(
        #     update={"nb_cells": nb_cells})       
        ...

    def _init_state(
            self,
            gloop: "GameLoop"
    ) -> None:
        bg_ = gloop._registry.init.img_assets['background']\
                                            .get_source('background')
        gloop._mlx.pygmlx_put_image_to_window(
            bg_.img,
            0,
            0
        )
        assets = gloop._registry.ingamestate
        # snapshot: GLMSnapshot = gloop._glm.view()
        # print(assets.img_assets["board"].sources)
        board_ = assets.img_assets["board"].get_source('board')
        gloop._drawer.draw(
                    board_.img,
                    gloop._glm.session.maze.grid,
                    None)
        if (board_.metadata and board_.metadata.x_pos_prop is not None
                and board_.metadata.y_pos_prop is not None):
            gloop._mlx.pygmlx_put_image_to_window(
                board_.img,
                board_.metadata.x_pos_prop,
                board_.metadata.y_pos_prop
                )
        level = gloop._glm.scoremng.player.level
        hub_bottom: ImgsAsset = gloop._assembler.text_loader_factdispatcher(
            "bottom_hub",
            "Level: {:>3}".format(str(level)),
            )
        hb_ = hub_bottom.get_source("bottom_hub")
        if (hb_.metadata and hb_.metadata.x_pos_prop is not None
                and hb_.metadata.y_pos_prop is not None):
            gloop._mlx.pygmlx_put_image_to_window(
                hb_.img,
                hb_.metadata.x_pos_prop,
                hb_.metadata.y_pos_prop
            )

    def _update_state(
            self,
            gloop: GameLoop,
            tick: int
    ) -> None:
        assets = gloop._registry.ingamestate
        snapshot: GLMSnapshot = gloop._glm.view()       
        # # snapshot = gloop._glm.session.timemng.view()
        # # str(gloop._glm.session.timemng._countdown_time_remaining)),
        # print(111, gloop._glm.session.timemng._discrete_cd_time)
        # print(111, gloop._glm.session.timemng._countdown_time_remaining)
        # print(111, gloop._glm.session.timemng._countdown_time_remaining)
        # print(111, gloop._glm.view().session.timemng.level_time)
        if gloop._glm.view().session.timemng.level_time is None:
            hub_top: ImgsAsset = gloop._assembler.text_loader_factdispatcher(
                "top_hub",
                "     STARTING AT {:>4}secs!!!! ".format(
                    str(gloop._glm.session.timemng._discrete_cd_time))
            )
            ht_ = hub_top.get_source("top_hub")
            if (ht_.metadata and ht_.metadata.x_pos_prop is not None
                    and ht_.metadata.y_pos_prop is not None):
                gloop._mlx.pygmlx_put_image_to_window(
                    ht_.img,
                    ht_.metadata.x_pos_prop,
                    ht_.metadata.y_pos_prop
                )
        else:
            score = gloop._glm.scoremng.player.score
            # INTERIOR CELLS ###
            # -- pacman --
            board_ = assets.img_assets["board"].get_source('board')
            gloop._drawer.draw_cell_interior(
                board_.img,
                gloop._glm.session.pacman.new_position,
                0xff000000
            )
            # # -- ghosts --
            # for g in gloop._glm.session.ghost_mng.ghosts:
            #     gloop._drawer.draw_cell_interior(
            #         board_asset.img,
            #         gloop._glm.session.ghost_mng.ghosts[g].old_position,
            #         0xff000000
            #     )
            for g in gloop._glm.session.ghost_mng.ghosts:
                gloop._drawer.draw_cell_interior(
                    board_.img,
                    gloop._glm.session.ghost_mng.ghosts[g].new_position,
                    0xff000000
                )
            if (board_.metadata and board_.metadata.x_pos_prop is not None
                    and board_.metadata.y_pos_prop is not None):
                gloop._mlx.pygmlx_put_image_to_window(
                    board_.img,
                    board_.metadata.x_pos_prop,
                    board_.metadata.y_pos_prop
                )
            # MENUS ###
            # # -- hub --
            if not tick % 60:
                hub_top: ImgsAsset = gloop._assembler\
                    .text_loader_factdispatcher(
                        "top_hub",
                        "Score: {:>8}    Remaining{:>4}secs".format(
                            str(score),
                            str(gloop._glm.view().session.timemng.level_time))
                    )
                ht_ = hub_top.get_source("top_hub")
                if (ht_.metadata and ht_.metadata.x_pos_prop is not None
                        and ht_.metadata.y_pos_prop is not None):
                    gloop._mlx.pygmlx_put_image_to_window(
                        ht_.img,
                        ht_.metadata.x_pos_prop,
                        ht_.metadata.y_pos_prop
                    )
            # # PACMAN ###
            pacman_steps = getattr(InGameState, 'PACMAN_STEPS')
            if not gloop._glm.session.pacman.new_direction:
                pD = (-1, 0)
            else:
                pD = gloop._glm.session.pacman.new_direction
            direction = [key.name
                         for key in pacman_steps if pacman_steps[key] == pD][0]
            print(direction)
            p_animations = assets.img_assets["pacman"].get_animation(direction)
            p_nextmove = p_animations.pop()
            # print(pm)
            gloop._mlx.pygmlx_put_image_to_window(
                p_nextmove.img,
                gloop._drawer.next_char_coord(
                                gloop._glm
                                .session
                                .pacman.new_position.cell_position_x),
                gloop._drawer.next_char_coord(
                                gloop._glm
                                .session
                                .pacman
                                .new_position
                                .cell_position_y) + gloop._drawer.bottom_h
            )
            if tick % 5 % gloop._glm.session.maze.nb_cells:
                p_animations.append(p_nextmove)
            else:
                p_animations.appendleft(p_nextmove)

            # # GHOSTS ###
            for g in gloop._glm.session.ghost_mng.ghosts:
                g_ = assets.img_assets["ghosts"].get_source(g.name)
                gloop._mlx.pygmlx_put_image_to_window(
                    g_.img,
                    gloop._drawer.next_char_coord(
                                gloop._glm
                                .session
                                .ghost_mng
                                .ghosts[g]
                                .new_position
                                .cell_position_x),
                    gloop._drawer.next_char_coord(
                                gloop._glm
                                .session
                                .ghost_mng
                                .ghosts[g]
                                .new_position
                                .cell_position_y) + gloop._drawer.bottom_h)
                    # gloop._drawer.next_char_coord(gloop._glm.session.ghost_mng.ghosts[g].new_position.cell_position_x) + int(gloop._drawer.next_char_coord(gloop._glm.session.ghost_mng.ghosts[g].new_position.cell_position_x) * gloop._glm.session.ghost_mng.ghosts[g].interpolation[0]),
                    # gloop._drawer.next_char_coord(gloop._glm.session.ghost_mng.ghosts[g].new_position.cell_position_y) + int(gloop._drawer.next_char_coord(gloop._glm.session.ghost_mng.ghosts[g].new_position.cell_position_y) * gloop._glm.session.ghost_mng.ghosts[g].interpolation[1]) + gloop._drawer.bottom_h
                    # gloop._drawer.next_char_coord(gloop._glm.session.ghost_mng.ghosts[g].new_position.cell_position_x + int(gloop._glm.session.ghost_mng.ghosts[g].new_position.cell_position_x * gloop._glm.session.ghost_mng.ghosts[g].interpolation[0])),
                    # gloop._drawer.next_char_coord(gloop._glm.session.ghost_mng.ghosts[g].new_position.cell_position_y + int(gloop._glm.session.ghost_mng.ghosts[g].new_position.cell_position_y * gloop._glm.session.ghost_mng.ghosts[g].interpolation[1])) + gloop._drawer.bottom_h


HANDLER_REGISTRY: dict[Type[IGameState], Type[IAction]] = {
    MainMenuState: MainMenuAction,
    InGameState: PlayingAction,
    GameOverPlayerLost: MainMenuAction
}


class GameLoop:
    def __init__(self,
                 mlx: PyGMiniLibXEmulator,
                 glm: GameLogicManager,
                 drawer: BoardDrawerEngine,
                 assembler: RendererAssembler,
                 assetregistry: AssetRegistry) -> None:
        self._registry: AssetRegistry = assetregistry
        self._mlx = mlx
        self._glm = glm
        self._drawer = drawer
        self._assembler = assembler
        self._currentstate: str = ""
        self._statechanged: bool = False
        self._currentlevel: int = 0
        self._levelchanged: bool = False
        self.event_queue: list[Event] = []

    def _actions(self,
                 msgs: EventMsg | None,
                 tick: int = 0) -> None:
        self._glm.update_logic(msgs)
        # ### introducing the game logic manager .view() function ###
        snapshot = self._glm.view()
        # print(snapshot.session.timemng)
        if isinstance(self._glm.state, IGameState):
            if (self._glm.state.__class__.__name__.lower()
                    != self._currentstate):
                self._currentstate = self._glm.state.__class__.__name__.lower()
                self._statechanged = True
            if snapshot.player.level != self._currentlevel:
                self._currentlevel = snapshot.player.level
                self._levelchanged = True
            print(self._statechanged)
            self._get_action(state=self._glm.state)().action(
                                            self,
                                            tick
                                            )
            self._statechanged = False
            self._levelchanged = False

    def state_loop(
            self,
            tick: int
    ) -> bool:
        msgs: EventMsg = {}
        current_assets: Assets = getattr(
            self._registry,
            self._currentstate
            if self._currentstate != "" else "mainmenustate")
        for event in self.event_queue:
            if event.type == pygame.QUIT:
                return False
            img_assets = list(current_assets.img_assets)
            for iass in img_assets:
                handler = current_assets.img_assets[iass].event_handler
                if handler is not None:
                    handler(event, msgs)
        self._actions(msgs, tick)
        return True

    def _get_action(
            self,
            state: IGameState,
            ) -> type[IAction]:
        return HANDLER_REGISTRY[type(state)]
