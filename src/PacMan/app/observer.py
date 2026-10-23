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

T = TypeVar("T", bound="IAction")
EventMsg: TypeAlias = dict[IEventEnums, dict[str, Any] | None] | None


class IAction(Protocol):
    def actions(self) -> None:
        ...


class PlayingAction:
    def action(self) -> None:
        print(f"this is {self.__class__.__name__}")


HANDLER_REGISTRY: dict[Type[IGameState], Type[IAction]] = {
    InGameState: PlayingAction
}


class Observer:
    def __init__(self,
                 glm: GameLogicManager,
                 drawer: "DrawerEngine") -> None:
        self._registry: dict[str, Any] | None = None
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
            self._get_action(state=self._glm.state)().action()

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
