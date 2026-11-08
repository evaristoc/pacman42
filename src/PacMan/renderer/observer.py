from __future__ import annotations
import pygame
from pygame import Event
from typing import TypeVar, Type, Any, Protocol, TYPE_CHECKING
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
    from src.PacMan.renderer.assets import ImgsAsset, AssetRegistry
    from src.PacMan.renderer.renderer_engine import PyGMiniLibXEmulator
    from src.PacMan.renderer.event_handlers import EventMsg
    from src.PacMan.renderer.renderer_assembler import RendererAssembler

T = TypeVar("T", bound="IAction")


class IAction(Protocol):
    def action(
            self,
            obs: "Observer",
            state: str,
            tick: int
            ) -> None:
        ...

    def _init_state(
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

class MainMenuAction(IAction):
    def action(
            self,
            obs: Observer,
            tick: int
    ) -> None:
        if obs._statechanged:
            self._init_state(obs)

    def _init_state(
            self,
            obs: Observer
    ) -> None:
        background = obs._mlx.pygmlx_new_image(
            obs._mlx.view_w,
            obs._mlx.view_h
        )
        obs._mlx.pygmlx_put_image_to_window(
            background,
            0,
            0
        )
        print(list(obs._registry.mainmenustate.img_assets['main'].sources.keys()))
        for s in obs._registry.mainmenustate.img_assets['main'].sources.values():
            obs._mlx.pygmlx_put_image_to_window(
                s.img,
                s.metadata.x_pos_prop,
                s.metadata.y_pos_prop
            )


class PlayingAction(IAction):
    # def _init_start(self,
    #                 obs: Observer) -> None:
    def action(
            self,
            obs: Observer,
            tick: int
    ) -> None:
        if obs._levelchanged:
            self._get_newlevel(obs)
        if obs._statechanged:
            self._init_state(obs)
        else:
            self._update_state(obs, tick)

    def _get_newlevel(
            self,
            obs: 'Observer'
    ) -> None:
        ...

    def _init_state(
            self,
            obs: "Observer"  
    ) -> None:
        background = obs._registry.init.img_assets['background'].sources['background']
        obs._mlx.pygmlx_put_image_to_window(
            background.img,
            0,
            0
        )
        assets = obs._registry.ingamestate
        # snapshot: GLMSnapshot = obs._glm.view()
        # print(assets.img_assets["board"].sources)
        board_asset = assets.img_assets["board"].sources["board"]
        obs._drawer.draw(board_asset.img,
                         obs._glm.session.maze.grid,
                         None)
        obs._mlx.pygmlx_put_image_to_window(
            board_asset.img,
            board_asset.metadata.x_pos_prop,
            board_asset.metadata.y_pos_prop
            )
        # hub_top = assets.img_assets["top_hub"].sources["top_hub"]

        # obs._mlx.pygmlx_put_image_to_window(
        #     hub_top.img,
        #     hub_top.metadata.x_pos_prop,
        #     hub_top.metadata.y_pos_prop
        #     )        

    def _update_state(
            self,
            obs: Observer,
            tick: int
    ) -> None:
        assets = obs._registry.ingamestate
        snapshot: GLMSnapshot = obs._glm.view()
        # INTERIOR CELLS ###
        # -- pacman --
        board_asset = assets.img_assets["board"].sources["board"]
        obs._drawer.draw_cell_interior(
            board_asset.img,
            obs._glm.session.pacman.new_position,
            0x000
        )
        # -- ghosts --

        for g in obs._glm.session.ghost_mng.ghosts:
            obs._drawer.draw_cell_interior(
                board_asset.img,
                obs._glm.session.ghost_mng.ghosts[g].new_position,
                0x000
            )
        obs._mlx.pygmlx_put_image_to_window(
            board_asset.img,
            board_asset.metadata.x_pos_prop,
            board_asset.metadata.y_pos_prop
        )
        # MENUS ###
        # # -- hub --
        # obs._mlx.pygmlx_put_image_to_window(
        #     obs._registry["menus"]["hub"],
        #     obs._drawer.margin / 2,
        #     obs._drawer.margin / 2 + obs._mlx.height
        # )
        if not tick % 60:
            hub_top: ImgsAsset = obs._assembler.text_loader_dispatcher(
                                        "top_hub",
                                        "Score: {:>8}    Remaining {:>4}secs".format(100, 90),
                                    )
            obs._mlx.pygmlx_put_image_to_window(
                hub_top.sources['top_hub'].img,
                hub_top.sources['top_hub'].metadata.x_pos_prop,
                hub_top.sources['top_hub'].metadata.y_pos_prop
            )      
        # # PACMAN ###
        pacman_steps = getattr(InGameState, 'PACMAN_STEPS')
        if not obs._glm.session.pacman.new_direction:
            pD = (-1, 0)
        else:
            pD = obs._glm.session.pacman.new_direction
        direction = [key.name
                     for key in pacman_steps if pacman_steps[key] == pD][0]
        print(direction)
        pm = assets.img_assets["pacman"].sources[direction].pop()
        # print(pm)
        obs._mlx.pygmlx_put_image_to_window(
            pm.img,
            obs._drawer.next_char_coord(obs._glm.session.pacman.new_position.cell_position_x),
            obs._drawer.next_char_coord(obs._glm.session.pacman.new_position.cell_position_y) + obs._drawer.bottom_h
        )
        if tick % 5:
            assets.img_assets["pacman"].sources[direction].append(pm)
        else:
            assets.img_assets["pacman"].sources[direction].appendleft(pm)

        # # GHOSTS ###
        for g in obs._glm.session.ghost_mng.ghosts:
            obs._mlx.pygmlx_put_image_to_window(
                assets.img_assets["ghosts"].sources[g.name].img,
                obs._drawer.next_char_coord(obs._glm.session.ghost_mng.ghosts[g].new_position.cell_position_x),
                obs._drawer.next_char_coord(obs._glm.session.ghost_mng.ghosts[g].new_position.cell_position_y) + obs._drawer.bottom_h
                # obs._drawer.next_char_coord(obs._glm.session.ghost_mng.ghosts[g].new_position.cell_position_x + int(obs._glm.session.ghost_mng.ghosts[g].new_position.cell_position_x * obs._glm.session.ghost_mng.ghosts[g].interpolation[0])),
                # obs._drawer.next_char_coord(obs._glm.session.ghost_mng.ghosts[g].new_position.cell_position_y + int(obs._glm.session.ghost_mng.ghosts[g].new_position.cell_position_y * obs._glm.session.ghost_mng.ghosts[g].interpolation[1])) + obs._drawer.bottom_h
            )

        # for i, img in enumerate(obs._registry["menus"]["start"].keys()):
        #     obs._mlx.pygmlx_put_image_to_window(
        #         obs._registry["menus"]["start"][img],
        #         int(obs._drawer.margin / 2) + 200,
        #         int(obs._drawer.margin / 2) + obs._drawer.bottom_h + i * 100
        #         )


HANDLER_REGISTRY: dict[Type[IGameState], Type[IAction]] = {
    MainMenuState: MainMenuAction,
    InGameState: PlayingAction,
    GameOverPlayerLost: MainMenuAction
}


class Observer:
    def __init__(self,
                 mlx: PyGMiniLibXEmulator,
                 glm: GameLogicManager,
                 drawer: BoardDrawerEngine,
                 assembler: RendererAssembler,
                 assetregistry: AssetRegistry) -> None:
        self._registry = assetregistry
        self._mlx = mlx
        self._glm = glm
        self._drawer = drawer
        self._assembler = assembler
        self._currentstate: str = ""
        self._statechanged: bool = False
        self._currentlevel: int = 0
        self._levelchanged: bool = False
        self.event_queue: list[Event] = []

    def register_assets(self, key: str, asset: dict[str, Any]) -> None:
        if not self._registry:
            self._registry = {}
        # print(asset)
        self._registry[key] = asset

    def _actions(self,
                 msgs: EventMsg | None,
                 tick: int = 0) -> None:
        self._glm.update_logic(msgs)
        # ### introducing the game logic manager .view() function ###
        snapshot = self._glm.view()
        # print(snapshot.session.timemng)
        if isinstance(self._glm.state, IGameState):
            if self._glm.state.__class__.__name__.lower() != self._currentstate:
                self._currentstate = self._glm.state.__class__.__name__.lower()
                self._statechanged = True
            if snapshot.player.level != self._currentlevel:
                self._currentlevel = snapshot.player.level
                self._levelchanged = True
            print(self._statechanged)
            # if self._glm.state.__class__.__name__.lower() == 'gameoverplayerlost':
            #     self._currentlevel = 1
            #     self._currentstate = 'ingamestate'
            #     self._levelchanged = False
            #     self._statechanged = False
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
        current_assets = getattr(
            self._registry,
            self._currentstate
            if self._currentstate != "" else "mainmenustate")
        for event in self.event_queue:
            if event.type == pygame.QUIT:
                return False
            current_assets.event_handler(event, msgs)
        self._actions(msgs, tick)
        return True

    def _get_action(
            self,
            state: IGameState,
            ) -> Type[T]:
        return HANDLER_REGISTRY[type(state)]

