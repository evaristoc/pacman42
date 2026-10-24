from __future__ import annotations
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
    def actions(self,
                assets,
                mlx: PyGMiniLibXEmulator,
                drawer: DrawerEngine,
                char_mng) -> None:
        ...


class PlayingAction:
    def action(
            self,
            obs: "Observer"
            ) -> None:
        print(f"this is {self.__class__.__name__}")
        print(obs._glm.character_manager.pacman.position)
        print(obs._glm.character_manager.ghost_mng.ghosts)
        obs._mlx.pygmlx_put_image_to_window(
            obs._registry["pacman"]["1"],
            obs.drawer.next_char_coord(obs._glm.character_manager.pacman.position[0]),
            obs.drawer.next_char_coord(obs._glm.character_manager.pacman.position[1])
        )
        for g in obs._glm.character_manager.ghost_mng.ghosts:
            n = ""
            if g.name == "BLINKY":
                n = "orange"
            if g.name == "CLYDE":
                n = "blue"
            if g.name == "INKY":
                n = "red"
            if g.name == "PINKY":
                n = "pink"
            obs._mlx.pygmlx_put_image_to_window(
                obs._registry["ghosts"][n],
                obs.drawer.next_char_coord(obs._glm.character_manager.ghost_mng.ghosts[g].position[0]),
                obs.drawer.next_char_coord(obs._glm.character_manager.ghost_mng.ghosts[g].position[1])
            )


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
        self.drawer = drawer

    def register_assets(self, key: str, asset: dict[str, Any]) -> None:
        if not self._registry:
            self._registry = {}
        print(asset)
        self._registry[key] = asset

    def actions(self,
                event: Event) -> None:
        eventmsg = self._translate_event(event)
        self._glm.update_logic(eventmsg)
        if isinstance(self._glm.state, IGameState):
            self.action = self._get_action(state=self._glm.state)().action(self)

    def _get_action(
            self,
            state: IGameState,
            ) -> Type[T]:
        return HANDLER_REGISTRY[type(state)]

    def _translate_event(self,
                         event: Event
                         ) -> EventMsg:
        events: EventMsg = {}
        if not events:
            return
        if event.K_DOWN:
            events[InGameEvents.PACMAN_SOUTH] = None
        if event.K_UP:
            events[InGameEvents.PACMAN_NORTH] = None
        if event.K_LEFT:
            events[InGameEvents.PACMAN_WEST] = None
        if event.K_RIGHT:
            events[InGameEvents.PACMAN_EAST] = None
