from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
from typing import Union
from src.PacMan.validation_contracts.event_enums import (IEventEnums,
                                                         InGameEvents)
from typing import Any

if TYPE_CHECKING:
    from src.PacMan.game_logic.gamemanager.gamelogicmng import GameLogicManager


class IGameState(ABC):
    def __init__(self, context: "GameLogicManager"):
        self.context: "GameLogicManager" = context
        print(f"GAME TRANSITION to {self.__class__.__name__}")

    @abstractmethod
    def update_logic(self,
                     events: dict[IEventEnums, dict[str, Any] | None] | None,
                     delta_ticks: int
                     ) -> Union["IGameState", None]:
        pass


class MainMenuState(IGameState):
    pass


class CheatingMenuState(IGameState):
    pass


class HighScoreMenuState(IGameState):
    pass


class PauseMenuState(IGameState):
    def update_logic(self,
                     events: dict[IEventEnums, dict[str, Any] | None] | None,
                     delta_ticks: int
                     ) -> Union["IGameState", None]:
        return


class InGameState(IGameState):
    def __init__(self, context: "GameLogicManager"):
        super().__init__(context=context)
        self.pacman_steps: dict[InGameEvents, tuple[int, int]] = {
            InGameEvents.PACMAN_NORTH: (0, -1),
            InGameEvents.PACMAN_SOUTH: (0, 1),
            InGameEvents.PACMAN_EAST: (1, 0),
            InGameEvents.PACMAN_WEST: (-1, 0),
        }

    def update_logic(self,
                     events: dict[IEventEnums, dict[str, Any] | None] | None,
                     delta_ticks: int
                     ) -> Union["IGameState", None]:
        if events:
            for event in events.keys():
                if not isinstance(event, InGameEvents):
                    raise ValueError(
                        f'{event} is not of type "InGameEvents"')
            event = self._get_priority_event(events)
            return self._process_event_enums(event, delta_ticks)
        else:
            self.context.character_manager.update(delta_ticks=delta_ticks)
        return None

    def _get_priority_event(self, events: dict) -> InGameEvents:
        # Define priority order
        priority_order = [InGameEvents.PAUSE,
                          InGameEvents.PACMAN_NORTH,
                          InGameEvents.PACMAN_EAST,
                          InGameEvents.PACMAN_SOUTH,
                          InGameEvents.PACMAN_WEST]

        for event in priority_order:
            if event in events:
                return event
        return list(events.keys())[0]

    def _process_event_enums(self,
                             event: InGameEvents,
                             delta_ticks: int
                             ) -> IGameState | None:

        if event in self.pacman_steps.keys():
            self._normal_ingame_update(delta_ticks=delta_ticks,
                                       pacman_move=self.pacman_steps.get(event))
            return None

        elif event == InGameEvents.PAUSE:
            return PauseMenuState(self.context)

        else:
            raise ValueError(f"Passed invalid event: {event} to"
                             " InGameState._process_event_enums.")

    def _normal_ingame_update(self, *,
                              delta_ticks: int,
                              pacman_move: tuple[int, int] | None = None
                              ) -> None:
        self.context.character_manager.update(pacman_move=pacman_move,
                                              delta_ticks=delta_ticks)
