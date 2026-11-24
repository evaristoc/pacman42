from __future__ import annotations
import logging
import pygame
from functools import partial
from pygame import Event
from dataclasses import dataclass
from types import MethodType
from typing import TypeVar, Type, Protocol, Callable, Optional, Self, Any, TYPE_CHECKING
from src.PacMan.game_logic.gamemanager.gamelogicmng import (
    GameLogicManager,
    GLMSnapshot)
from src.PacMan.validation_contracts.event_enums import (
    IEventEnums,
    InGameEvents)
from src.PacMan.game_logic.ingame.characters.ghosts.ghosts import (
    GhostName)
from src.PacMan.game_logic.gamemanager.game_sm import (
                                            IGameState,
                                            MainMenuState,
                                            InGameState,
                                            GameOverPlayerLost,
                                            GameOverPlayerWon,
                                            PauseMenuState,
                                            InstructionsMenuState,
                                            HighScoreRegisterState,
                                            HighScoreMenuState,
                                            RegisterMenuState)
from src.PacMan.renderer.event_handlers import pacman_eh
if TYPE_CHECKING:  # only required for parameter type assignment
    from src.PacMan.renderer.assets import ImgsAsset, Assets, AssetRegistry
    from src.PacMan.renderer.renderer_engine import PyGMiniLibXEmulator
    from src.PacMan.renderer.event_handlers import EventMsg
    from src.PacMan.renderer.renderer_assembler import RendererAssembler

logger = logging.getLogger(__name__)


T = TypeVar("T", bound="IAction")


@dataclass
class InputDTO:
    handler: Optional[Callable[[ImgsAsset, pygame.event.Event, dict[IEventEnums, dict[str, Any] | None] | None], None]] = None
    event: Optional[pygame.event.Event] = None
    msgs: Optional[EventMsg] = None


class IAction(Protocol):
    def action(
            self,
            gloop: "GameLoop",
            tick: int
    ) -> None:
        ...

    # def _init_state(
    #         self,
    #         gloop: "GameLoop"
    # ) -> None:
    #     ...


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
            bg_ = gloop._registry.init.img_assets['background']\
                .get_source('background')
            gloop._mlx.pygmlx_put_image_to_window(
                bg_.img,
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


class InstructionMenuAction(IAction):
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
            bg_ = gloop._registry.init.img_assets['background']\
                .get_source('background')
            gloop._mlx.pygmlx_put_image_to_window(
                bg_.img,
                0,
                0
            )
            txt_ = gloop\
                ._registry\
                .instructionsmenustate\
                .img_assets["text"].get_source(
                    "instructions_text"
                )
            if (txt_.metadata and txt_.metadata.x_pos_prop is not None
                    and txt_.metadata.y_pos_prop is not None):
                gloop._mlx.pygmlx_put_image_to_window(
                    txt_.img,
                    txt_.metadata.x_pos_prop,
                    txt_.metadata.y_pos_prop
                )
            b_ = gloop\
                ._registry\
                .instructionsmenustate\
                .img_assets["return"].get_source(
                    "RETURN"
                    )
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


class LeaderboardMenuAction(IAction):
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
            snapshot = gloop._glm.view()
            # snapshot.highscore
            # if highscore empty, show a message is empty
            bg_ = gloop._registry.init.img_assets['background']\
                .get_source('background')
            gloop._mlx.pygmlx_put_image_to_window(
                bg_.img,
                0,
                0
            )
            # txt_ = gloop\
            #     ._registry\
            #     .highscoremenustate\
            #     .img_assets["text"].get_source(
            #         "leaderboard_table"
            #     )
            header = f"     {'rank':<3} | {'username':<10} | {'score':<5}"
            separator = "     " + "-" * len(header)
            # print(snapshop.game_state)
            # leader_list = [f"{rank:<3} | {username:<10} | {score:05d}"
            #                for rank, username, score
            #                in snapshop.highscores]
            mock_scores = [
                (1, "Alice", 1500),
                (2, "Bob", 1200),
                (3, "Charlie", 950),
            ]
            # NOTE for size === 750
            header_txt = "\n".join([header, separator])
            header_: ImgsAsset = gloop\
                ._assembler.text_loader_factdispatcher(
                        "leaderboard",
                        header_txt,
                )
            h_ = header_.get_source("leaderboard")
            rank_list = [f"    {alldata[0]:<3}"
                         for alldata
                         in mock_scores]
            h_.img.pygput_from_text(
                10,
                100,
                "\n".join(rank_list)
            )
            user_list = [f"{alldata[1]:<10}"
                         for alldata
                         in mock_scores]
            h_.img.pygput_from_text(
                200,
                100,
                "\n".join(user_list)
            )
            score_list = [f"{' ' * (10 - len(str(alldata[2])))}{alldata[2]}"
                          for alldata
                          in mock_scores]
            h_.img.pygput_from_text(
                400,
                100,
                "\n".join(score_list)
            )
            if (h_.metadata and h_.metadata.x_pos_prop is not None
                    and h_.metadata.y_pos_prop is not None):
                gloop._mlx.pygmlx_put_image_to_window(
                    h_.img,
                    h_.metadata.x_pos_prop,
                    h_.metadata.y_pos_prop
                )
            b_ = gloop\
                ._registry\
                .instructionsmenustate\
                .img_assets["return"].get_source(
                    "RETURN"
                    )
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


class PauseMenuAction(IAction):
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
            bg_ = gloop._registry.init.img_assets['background']\
                .get_source('background')
            gloop._mlx.pygmlx_put_image_to_window(
                bg_.img,
                0,
                0
            )
            buttons = list(gloop._registry.pausemenustate.img_assets['pause']
                           .sources.keys())
            for button in buttons:
                b_ = gloop._registry.pausemenustate.img_assets['pause']\
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


class RegisterMenuAction(IAction):
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
            buttons = list(
                gloop._registry
                .highscoreregisterstate.img_assets['register']
                .sources.keys())
            for button in buttons:
                b_ = gloop._registry\
                    .highscoreregisterstate.img_assets['register']\
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


# class RegisterMenuAction(IAction):
#     def action(
#             self,
#             gloop: GameLoop,
#             tick: int
#     ) -> None:
#         _ = tick
#         if gloop._statechanged:
#             self._init_state(gloop)

#     def _init_state(
#             self,
#             gloop: GameLoop
#     ) -> None:
#         try:
#             background = gloop._mlx.pygmlx_new_image(
#                 gloop._mlx.view_w,
#                 gloop._mlx.view_h
#             )
#             gloop._mlx.pygmlx_put_image_to_window(
#                 background,
#                 0,
#                 0
#             )
#             buttons = list(
#                 gloop._registry
#                 .highscoreregisterstate.img_assets['register']
#                 .sources.keys())
#             for button in buttons:
#                 b_ = gloop._registry\
#                     .highscoreregisterstate.img_assets['register']\
#                     .get_source(button)
#                 if (b_.metadata and b_.metadata.x_pos_prop is not None
#                         and b_.metadata.y_pos_prop is not None):
#                     gloop._mlx.pygmlx_put_image_to_window(
#                         b_.img,
#                         b_.metadata.x_pos_prop,
#                         b_.metadata.y_pos_prop
#                     )
#         except Exception as err:
#             logger.error(f"FATAL: Exception trying to load menus: {err}")
#             raise SystemExit(1)


class InputAction(IAction):
    def action(
            self,
            gloop: GameLoop,
            tick: int
    ) -> None:
        # TODO Handler for input should be INSIDE it s action!!!
        # TODO Paint only a small piece! Not the whole background
        _ = tick
        try:
            bg_ = gloop._registry.init.img_assets['background']\
                .get_source('background')
            gloop._mlx.pygmlx_put_image_to_window(
                bg_.img,
                0,
                0
            )
            txt_ = gloop\
                ._registry\
                .registermenustate\
                .img_assets["input_text"].get_source(
                    "input_text"
                )
            if (txt_.metadata and txt_.metadata.x_pos_prop is not None
                    and txt_.metadata.y_pos_prop is not None):
                gloop._mlx.pygmlx_put_image_to_window(
                    txt_.img,
                    txt_.metadata.x_pos_prop,
                    txt_.metadata.y_pos_prop
                )
        except Exception as err:
            logger.error(f"FATAL: Exception trying to load menus: {err}")
            raise SystemExit(1)


class GameOverWonAction(IAction):
    def action(
            self,
            gloop: GameLoop,
            tick: int
    ) -> None:
        _ = tick
        gow_ = gloop._registry\
            .gameoverplayerwon.img_assets['gameoverwon']\
                    .get_source('WON')
        if (gow_.metadata and gow_.metadata.x_pos_prop is not None
                and gow_.metadata.y_pos_prop is not None):
            gloop._mlx.pygmlx_put_image_to_window(
                gow_.img,
                gow_.metadata.x_pos_prop,
                gow_.metadata.y_pos_prop
            )


class GameOverLostAction(IAction):
    def action(
            self,
            gloop: GameLoop,
            tick: int
    ) -> None:
        _ = tick
        gow_ = gloop._registry\
            .gameoverplayerlost.img_assets['gameoverlost']\
                    .get_source('LOST')
        if (gow_.metadata and gow_.metadata.x_pos_prop is not None
                and gow_.metadata.y_pos_prop is not None):
            gloop._mlx.pygmlx_put_image_to_window(
                gow_.img,
                gow_.metadata.x_pos_prop,
                gow_.metadata.y_pos_prop
            )


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
        self._update_state(gloop, tick)

    def _get_newlevel(
            self,
            gloop: 'GameLoop'
    ) -> None:
        # # TODO update nb_cells config before drawer
        # # NOTE I need to compute before loading, need those values
        # self.drawer.compute(gloop._assembler._config)
        # gloop._assembler.drawer.basic_calcs()
        # nb_cells = self.glm.session.maze.nb_cells
        snapshot: GLMSnapshot = gloop._glm.view()
        nb_cells = -1
        if snapshot.session and snapshot.session.maze is not None:
            nb_cells = snapshot.session.maze.nb_cells
        gloop._assembler._config = gloop._assembler._config.model_copy(
            update={"nb_cells": nb_cells})
        gloop._assembler.init_drawer()
        board_: ImgsAsset = gloop._assembler\
            .img_loader_factdispatcher(
                "board",
                gloop._assembler.drawer)
        ghosts_: ImgsAsset = gloop._assembler\
            .img_loader_factdispatcher(
                "ghosts",
                GhostName)
        pacman_: ImgsAsset = gloop._assembler\
            .img_loader_factdispatcher(
                "pacman",
                InGameEvents)
        pacman_.event_handler = MethodType(pacman_eh, pacman_)
        assets = gloop._registry.ingamestate
        assets.img_assets['board'] = board_
        assets.img_assets['ghosts'] = ghosts_
        assets.img_assets['pacman'] = pacman_
        self._init_state(gloop)

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
        snapshot: GLMSnapshot = gloop._glm.view()
        # print(assets.img_assets["board"].sources)
        board_ = assets.img_assets["board"].get_source('board')
        if snapshot.session:
            gloop._assembler.drawer.draw(
                board_.img,
                snapshot.session.maze.grid,
                None)
        if (board_.metadata and board_.metadata.x_pos_prop is not None
                and board_.metadata.y_pos_prop is not None):
            gloop._mlx.pygmlx_put_image_to_window(
                board_.img,
                board_.metadata.x_pos_prop,
                board_.metadata.y_pos_prop
            )
        level = gloop._glm.scoremng.player.level
        print(level)
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
        for i in range(gloop._assembler._config.lives):
            l_ = assets.img_assets["live"].get_source(f"LIVE_{i}")
            if (l_.metadata.x_pos_prop is not None
                    and l_.metadata.y_pos_prop is not None):
                gloop._mlx.pygmlx_put_image_to_window(
                    l_.img,
                    l_.metadata.x_pos_prop,
                    l_.metadata.y_pos_prop
                )

    def _update_state(
            self,
            gloop: GameLoop,
            tick: int
    ) -> None:
        assets = gloop._registry.ingamestate
        snapshot: GLMSnapshot = gloop._glm.view()
        if (
            snapshot is not None and
            snapshot.session is not None and
            snapshot.session.timemng is not None and
            snapshot.session.pacman is not None
        ):
            hub_top: ImgsAsset
            if snapshot.session.timemng.level_time is None:
                hub_top = gloop._assembler\
                    .text_loader_factdispatcher(
                        "top_hub",
                        "     STARTING AT {:>4}    !!!! ".format(
                            str(snapshot.session.timemng.countdown_time))
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
                score = snapshot.player.score
                # ======> LAST STATES : NOT CHARACTERS!! <=========
                # INTERIOR CELLS ###
                # -- last STATE of the board -- #
                board_ = assets.img_assets["board"].get_source('board')
                # -- pacman: last state of the pellets --
                gloop._assembler.drawer.draw_cell_interior(
                    board_.img,
                    snapshot.session.pacman.next_tile,
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
                    hub_top = gloop._assembler\
                        .text_loader_factdispatcher(
                            "top_hub",
                            "Score: {:>8}   Remaining{:>4}secs".format(
                                str(score),
                                str(snapshot.session.timemng.level_time))
                        )
                    ht_ = hub_top.get_source("top_hub")
                    if (ht_.metadata and ht_.metadata.x_pos_prop is not None
                            and ht_.metadata.y_pos_prop is not None):
                        gloop._mlx.pygmlx_put_image_to_window(
                            ht_.img,
                            ht_.metadata.x_pos_prop,
                            ht_.metadata.y_pos_prop
                        )
                if snapshot.player.lives < gloop._assembler._config.lives:
                    blacking = snapshot.player.lives
                    l_ = assets.img_assets["live"].get_source(
                        f"LIVE_{str(blacking)}")
                    blck_ = assets.img_assets["live"].get_source("blacking")
                    if (l_.metadata.x_pos_prop is not None
                            and l_.metadata.y_pos_prop is not None):
                        gloop._mlx.pygmlx_put_image_to_window(
                            blck_.img,
                            l_.metadata.x_pos_prop,
                            l_.metadata.y_pos_prop
                        )
                # # PACMAN ###
                pacman_steps = getattr(InGameState, 'PACMAN_STEPS')
                if not snapshot.session.pacman.direction:
                    pD = (-1, 0)
                else:
                    pD = snapshot.session.pacman.direction
                direction = [key.name
                             for key in pacman_steps
                             if pacman_steps[key] == pD][0]
                # print(direction)
                p_animations = assets.img_assets["pacman"]\
                    .get_animation(direction)
                p_nextmove = p_animations.pop()
                # print(pm)
                gloop._mlx.pygmlx_put_image_to_window(
                    p_nextmove.img,
                    gloop._assembler.drawer.next_char_coord(
                        snapshot
                                    .session
                                    .pacman
                                    .next_tile
                                    .cell_position_x),
                    gloop._assembler.drawer.next_char_coord(
                        snapshot
                                    .session
                                    .pacman
                                    .next_tile
                                    .cell_position_y) +
                    gloop._assembler.drawer.bottom_h
                )
                if tick % 5 % snapshot.session.maze.nb_cells:
                    p_animations.append(p_nextmove)
                else:
                    p_animations.appendleft(p_nextmove)

                # # GHOSTS ###
                for g, ss in snapshot\
                        .session.ghost_mng.ghost_snapshots.items():
                    if ss.state == 'FrightenedGhostState':
                        g_ = assets.img_assets["ghosts"].get_source('POWERUP')
                    elif ss.state == 'EatenGhostState':
                        g_ = assets.img_assets["ghosts"].get_source('DEAD')
                    else:
                        g_ = assets.img_assets["ghosts"].get_source(g)
                    gloop._mlx.pygmlx_put_image_to_window(
                        g_.img,
                        gloop._assembler.drawer.next_char_coord(
                            snapshot
                            .session
                            .ghost_mng
                            .ghost_snapshots[g]
                            .previous_tile
                            .cell_position_x,
                            True,
                            snapshot
                            .session
                            .ghost_mng
                            .ghost_snapshots[g]
                            .interpolation[0]
                        ),
                        gloop._assembler.drawer.next_char_coord(
                            snapshot
                            .session
                            .ghost_mng
                            .ghost_snapshots[g]
                            .previous_tile
                            .cell_position_y,
                            True,
                            snapshot
                            .session
                            .ghost_mng
                            .ghost_snapshots[g]
                            .interpolation[1]
                        ) + gloop._assembler.drawer.bottom_h)


HANDLER_REGISTRY: dict[Type[IGameState], Type[IAction]] = {
    MainMenuState: MainMenuAction,
    InGameState: PlayingAction,
    GameOverPlayerLost: GameOverLostAction,
    GameOverPlayerWon: GameOverWonAction,
    HighScoreRegisterState: RegisterMenuAction,
    PauseMenuState: PauseMenuAction,
    InstructionsMenuState: InstructionMenuAction,
    HighScoreMenuState: LeaderboardMenuAction,
    RegisterMenuState: InputAction
}


class GameLoop:
    def __init__(self,
                 mlx: PyGMiniLibXEmulator,
                 glm: GameLogicManager,
                 assembler: RendererAssembler,
                 assetregistry: AssetRegistry) -> None:
        self._registry: AssetRegistry = assetregistry
        self._mlx = mlx
        self._glm = glm
        self._assembler = assembler
        self._currentstate: str = ""
        self._statechanged: bool = False
        self._currentlevel: int = 0
        self._levelchanged: bool = False
        self.event_queue: list[Event] = []
        self.bus: InputDTO = InputDTO()

    def _actions(self,
                 msgs: EventMsg | None,
                 tick: int = 0) -> None:
        self._glm.update_logic(msgs)
        # ### introducing the game logic manager .view() function ###
        snapshot = self._glm.view()
        if isinstance(self._glm.state, IGameState):
            if (self._glm.state.__class__.__name__.lower()
                    != self._currentstate):
                self._currentstate = self._glm.state.__class__.__name__.lower()
                self._statechanged = True
            if snapshot.player.level != self._currentlevel:
                self._currentlevel = snapshot.player.level
                self._levelchanged = True
            # print(self._statechanged)
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
                    if self._currentstate != "registermenustate":
                        handler(event, msgs)
                    else:
                        # TODO MAKE A SMALL BUS HERE...
                        # I need a vehicle that keep the data and it is run by the action, so THIS could be an observer...
                        i = 0
        self._actions(msgs, tick)
        return True

    def _get_action(
            self,
            state: IGameState,
    ) -> type[IAction]:
        return HANDLER_REGISTRY[type(state)]
