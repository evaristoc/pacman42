from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
from typing import Union
from src.PacMan.validation_contracts.event_enums import (IEventEnums,
                                                         InGameEvents,
                                                         PauseMenuEvents,
                                                         MainMenuEvents,
                                                         InstructionMenuEvents,
                                                         HighScoreMenuEvents,
                                                         HighScoreRegisterEvents)
from typing import Any
from src.PacMan.game_logic.ingame.update_outcome import UpdateOutcome
if TYPE_CHECKING:
    from src.PacMan.game_logic.gamemanager.gamelogicmng import GameLogicManager
import sys

MAX_LEVEL = 3


class GameStateError(Exception):
    pass


class IGameState(ABC):
    def __init__(self, context: "GameLogicManager"):
        self.context: "GameLogicManager" = context

    @abstractmethod
    def update_logic(self,
                     events: dict[IEventEnums, dict[str, Any] | None] | None,
                     delta_ticks: int
                     ) -> Union["IGameState", None]:
        pass

    def _validate_events(self,
                         events: dict[IEventEnums, dict[str, Any] | None],
                         state_events: type
                         ) -> IEventEnums:
        if not isinstance(events, dict):
            raise ValueError(f"{events} is not a dictionary..")
        for event, value in events.items():
            if not isinstance(event, state_events):
                raise ValueError(
                    f'{event} is not of type "{state_events.__name__}"')
            if value is not None and not isinstance(value, dict):
                raise ValueError(f"{value} is not a dictionary.")
        return self._get_priority_event(events)

    @staticmethod
    @abstractmethod
    def _get_priority_event(events: dict[IEventEnums, dict[str, Any] | None]
                            ) -> IEventEnums:
        pass


class MainMenuState(IGameState):
    def __init__(self, context: "GameLogicManager"):
        self.context: "GameLogicManager" = context

    def update_logic(self,
                     events: dict[IEventEnums, dict[str, Any] | None] | None,
                     delta_ticks: int
                     ) -> Union["IGameState", None]:
        if events:
            event = self._validate_events(events, MainMenuEvents)
            if event == MainMenuEvents.EXIT:
                sys.exit()
            elif event == MainMenuEvents.START:
                return InGameState(self.context)
            elif event == MainMenuEvents.INSTRUCTIONS:
                return InstructionsMenuState(self.context)
            elif event == MainMenuEvents.HIGHSCORES:
                return HighScoreMenuState(self.context)

        return None

    @staticmethod
    def _get_priority_event(events: dict[IEventEnums, dict[str, Any] | None]
                            ) -> IEventEnums:
        priority_order = [MainMenuEvents.EXIT,
                          MainMenuEvents.START,
                          MainMenuEvents.INSTRUCTIONS,
                          MainMenuEvents.HIGHSCORES]

        for event in priority_order:
            if event in events:
                return event
        return list(events.keys())[0]


class InstructionsMenuState(IGameState):
    def __init__(self, context: "GameLogicManager"):
        self.context: "GameLogicManager" = context

    def update_logic(self,
                     events: dict[IEventEnums, dict[str, Any] | None] | None,
                     delta_ticks: int
                     ) -> Union["IGameState", None]:
        if events:
            event = self._validate_events(events, InstructionMenuEvents)
            if event == InstructionMenuEvents.RETURN:
                return MainMenuState(self.context)

        return None

    @staticmethod
    def _get_priority_event(events: dict[IEventEnums, dict[str, Any] | None]
                            ) -> IEventEnums:
        priority_order = [InstructionMenuEvents.RETURN]

        for event in priority_order:
            if event in events:
                return event
        return list(events.keys())[0]


class HighScoreMenuState(IGameState):
    def __init__(self, context: "GameLogicManager"):
        self.context: "GameLogicManager" = context

    def update_logic(self,
                     events: dict[IEventEnums, dict[str, Any] | None] | None,
                     delta_ticks: int
                     ) -> Union["IGameState", None]:
        if events:
            event = self._validate_events(events, HighScoreMenuEvents)
            if event == HighScoreMenuEvents.RETURN:
                return MainMenuState(self.context)
        return None

    @staticmethod
    def _get_priority_event(events: dict[IEventEnums, dict[str, Any] | None]
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
            event = self._validate_events(events, PauseMenuEvents)
            if event == PauseMenuEvents.CONTINUE:
                return InGameState(self.context)
            elif event == PauseMenuEvents.EXIT:
                self.context.session = None
                return HighScoreRegisterState(self.context)
        return None

    @staticmethod
    def _get_priority_event(events: dict[IEventEnums, dict[str, Any] | None]
                            ) -> IEventEnums:
        priority_order = [PauseMenuEvents.EXIT,
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
                event = self._validate_events(events, InGameEvents)
                return self._process_event_enums(event, delta_ticks)
            else:
                return self._normal_ingame_update(delta_ticks=delta_ticks)
        return None

    @staticmethod
    def _get_priority_event(events: dict[IEventEnums, dict[str, Any] | None]
                            ) -> IEventEnums:
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
            outcome: UpdateOutcome = self.context.session.update(pacman_move=pacman_move,
                                                                 delta_ticks=delta_ticks)
            if not outcome.value[0]:
                return None

            if outcome.value[1] and not self.context.final_level():
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

    def update_logic(self,
                     events: dict[IEventEnums, dict[str, Any] | None] | None,
                     delta_ticks: int
                     ) -> Union["IGameState", None]:
        if events:
            event = self._validate_events(events, HighScoreRegisterEvents)
            if event == HighScoreRegisterEvents.CANCEL:
                return MainMenuState(self.context)
            elif event == HighScoreRegisterEvents.REGISTER:
                event_dict: dict[str,
                                 Any] | None = events[HighScoreRegisterEvents.REGISTER]
                if event_dict:
                    self.context.player.set_name(event_dict['name'])
                return MainMenuState(self.context)

        return None

    @staticmethod
    def _get_priority_event(events: dict[IEventEnums, dict[str, Any] | None]
                            ) -> IEventEnums:
        priority_order = [HighScoreRegisterEvents.CANCEL,
                          HighScoreRegisterEvents.REGISTER]

        for event in priority_order:
            if event in events:
                return event
        return list(events.keys())[0]
