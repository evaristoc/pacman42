from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
from typing import Union
from src.PacMan.validation_contracts.event_enums import (IEventEnums,
                                                         InGameEvents,
                                                         PauseMenuEvents,
                                                         MainMenuEvents,
                                                         CheatingMenuEvents,
                                                         HighScoreMenuEvents,
                                                         HighScoreRegisterEvents)
from typing import Any
if TYPE_CHECKING:
    from src.PacMan.game_logic.gamemanager.gamelogicmng import GameLogicManager
import sys

MAX_LEVEL = 3


class GameStateError(Exception):
    pass


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
    def __init__(self, context: "GameLogicManager"):
        self.context: "GameLogicManager" = context
        print(f"GAME TRANSITION to {self.__class__.__name__}")

    def update_logic(self,
                     events: dict[IEventEnums, dict[str, Any] | None] | None,
                     delta_ticks: int
                     ) -> Union["IGameState", None]:
        if events:
            for event in events.keys():
                if not isinstance(event, MainMenuEvents):
                    raise ValueError(
                        f'{event} is not of type "MainMenuEvents"')
            event = self._get_priority_event(events)
            if event == MainMenuEvents.QUIT:
                sys.exit()
            elif event == MainMenuEvents.START:
                return InGameState(self.context)
            elif event == MainMenuEvents.CHEATING:
                return CheatingMenuState(self.context)
            elif event == MainMenuEvents.HIGHSCORES:
                return HighScoreMenuState(self.context)

        return None

    def _get_priority_event(self,
                            events: dict[IEventEnums, dict[str, Any] | None]
                            ) -> IEventEnums:
        priority_order = [MainMenuEvents.QUIT,
                          MainMenuEvents.START,
                          MainMenuEvents.CHEATING,
                          MainMenuEvents.HIGHSCORES]

        for event in priority_order:
            if event in events:
                return event
        return list(events.keys())[0]


class CheatingMenuState(IGameState):
    def __init__(self, context: "GameLogicManager"):
        self.context: "GameLogicManager" = context
        print(f"GAME TRANSITION to {self.__class__.__name__}")

    def update_logic(self,
                     events: dict[IEventEnums, dict[str, Any] | None] | None,
                     delta_ticks: int
                     ) -> Union["IGameState", None]:
        if events:
            for event in events.keys():
                if not isinstance(event, CheatingMenuEvents):
                    raise ValueError(
                        f'{event} is not of type "CheatingMenuEvents"')
            event = self._get_priority_event(events)
            if event == CheatingMenuEvents.RETURN:
                return MainMenuState(self.context)
            elif event == CheatingMenuEvents.IMPOTENTGHOSTS:
                self.context.toggle_impotent_ghosts()
                return None

        return None

    def _get_priority_event(self,
                            events: dict[IEventEnums, dict[str, Any] | None]
                            ) -> IEventEnums:
        priority_order = [CheatingMenuEvents.RETURN,
                          CheatingMenuEvents.IMPOTENTGHOSTS]

        for event in priority_order:
            if event in events:
                return event
        return list(events.keys())[0]


class HighScoreMenuState(IGameState):
    def __init__(self, context: "GameLogicManager"):
        self.context: "GameLogicManager" = context
        print(f"GAME TRANSITION to {self.__class__.__name__}")

    def update_logic(self,
                     events: dict[IEventEnums, dict[str, Any] | None] | None,
                     delta_ticks: int
                     ) -> Union["IGameState", None]:
        if events:
            for event in events.keys():
                if not isinstance(event, HighScoreMenuEvents):
                    raise ValueError(
                        f'{event} is not of type "HighScoreMenuEvents"')
            event = self._get_priority_event(events)
            if event == HighScoreMenuEvents.RETURN:
                return MainMenuState(self.context)

        return None

    def _get_priority_event(self,
                            events: dict[IEventEnums, dict[str, Any] | None]
                            ) -> IEventEnums:
        priority_order = [HighScoreMenuEvents.RETURN]

        for event in priority_order:
            if event in events:
                return event
        return list(events.keys())[0]


class PauseMenuState(IGameState):
    def __init__(self, context: "GameLogicManager"):
        super().__init__(context=context)
        if self.context.session:
            if self.context.session.timemng:
                self.context.session.timemng.pause()
            else:
                raise GameStateError("Passed in to PauseMenuState"
                                     " without an instantiated time manager.")

    def update_logic(self,
                     events: dict[IEventEnums, dict[str, Any] | None] | None,
                     delta_ticks: int
                     ) -> Union["IGameState", None]:
        if events:
            for event in events.keys():
                if not isinstance(event, PauseMenuEvents):
                    raise ValueError(
                        f'{event} is not of type "PauseMenuEvents"')
            event = self._get_priority_event(events)
            if event == PauseMenuEvents.CONTINUE:
                return InGameState(self.context)
            elif event == PauseMenuEvents.QUIT:
                return HighScoreRegisterState(self.context)
        return None

    def _get_priority_event(self,
                            events: dict[IEventEnums, dict[str, Any] | None]
                            ) -> IEventEnums:
        priority_order = [PauseMenuEvents.QUIT,
                          PauseMenuEvents.CONTINUE]

        for event in priority_order:
            if event in events:
                return event
        return list(events.keys())[0]


class InGameState(IGameState):
    PACMAN_STEPS: dict[IEventEnums, tuple[int, int]] = {
        InGameEvents.PACMAN_NORTH: (0, -1),
        InGameEvents.PACMAN_SOUTH: (0, 1),
        InGameEvents.PACMAN_EAST: (1, 0),
        InGameEvents.PACMAN_WEST: (-1, 0),
    }

    def __init__(self, context: "GameLogicManager"):
        super().__init__(context=context)
        if not self.context.session:
            self.context.session = self.context.create_game_session()
        else:
            self.context.session.timemng.start()

    def update_logic(self,
                     events: dict[IEventEnums, dict[str, Any] | None] | None,
                     delta_ticks: int
                     ) -> Union["IGameState", None]:
        if self.context.session:
            if events:
                for event in events.keys():
                    if not isinstance(event, InGameEvents):
                        raise ValueError(
                            f'{event} is not of type "InGameEvents"')
                event = self._get_priority_event(events)
                return self._process_event_enums(event, delta_ticks)
            else:
                return self._normal_ingame_update(delta_ticks=delta_ticks)
        return None

    def _get_priority_event(self, events: dict[IEventEnums, dict[str, Any] | None]) -> IEventEnums:
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
                             event: IEventEnums,
                             delta_ticks: int
                             ) -> IGameState | None:
        if event in self.PACMAN_STEPS.keys():
            return self._normal_ingame_update(delta_ticks=delta_ticks,
                                              pacman_move=self.PACMAN_STEPS.get(event))
        elif event == InGameEvents.PAUSE:
            return PauseMenuState(self.context)
        else:
            raise ValueError(f"Passed invalid event: {event} to"
                             " InGameState._process_event_enums.")

    def _normal_ingame_update(self, *,
                              delta_ticks: int,
                              pacman_move: tuple[int, int] | None = None
                              ) -> IGameState | None:
        if self.context.session:
            game_over, level_won = self.context.session.update(pacman_move=pacman_move,
                                                               delta_ticks=delta_ticks)
            if not game_over:
                return None

            if level_won and not self.context.final_level():
                self._increment_level()
                return None

            self.context.session = None
            return HighScoreRegisterState(self.context)

        return None

    def _increment_level(self) -> None:
        if self.context.player.level == MAX_LEVEL:
            raise RuntimeError(
                "Can't increment level. Level is already final level.")
        self.context.player.level += 1
        self.context.session = self.context.create_game_session()
        self.context.state = InGameState(self.context)


class HighScoreRegisterState(InGameState):
    def __init__(self, context: "GameLogicManager"):
        self.context: "GameLogicManager" = context
        print("GAAAMEEE OVERRRRRR")
        print(f"GAME TRANSITION to {self.__class__.__name__}")

    def update_logic(self,
                     events: dict[IEventEnums, dict[str, Any] | None] | None,
                     delta_ticks: int
                     ) -> Union["IGameState", None]:
        if events:
            for event in events.keys():
                if not isinstance(event, HighScoreRegisterEvents):
                    raise ValueError(
                        f'{event} is not of type "HighScoreRegisterEvents"')
            event = self._get_priority_event(events)
            if event == HighScoreRegisterEvents.CANCEL:
                return MainMenuState(self.context)
            elif event == HighScoreRegisterEvents.REGISTER:
                event_dict: dict[str,
                                 Any] | None = events[HighScoreRegisterEvents.REGISTER]
                if event_dict:
                    self.context.player.set_name(event_dict['name'])
                return MainMenuState(self.context)

        return None

    def _get_priority_event(self,
                            events: dict[IEventEnums, dict[str, Any] | None]
                            ) -> IEventEnums:
        priority_order = [HighScoreRegisterEvents.CANCEL,
                          HighScoreRegisterEvents.REGISTER]

        for event in priority_order:
            if event in events:
                return event
        return list(events.keys())[0]
