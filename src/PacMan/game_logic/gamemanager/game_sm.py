from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
from typing import Union
from src.PacMan.validation_contracts.event_enums import InGameEvents

if TYPE_CHECKING:
    from src.PacMan.game_logic.gamemanager.gamelogicmng import GameLogicManager


class IGameState(ABC):
    def __init__(self, context: "GameLogicManager"):
        self.context: "GameLogicManager" = context
        print(f"GAME TRANSITION to {self.__class__.__name__}")

    @abstractmethod
    def update_logic(self,
                     events: list | None,
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
                     events: list | None,
                     delta_ticks: int
                     ) -> Union["IGameState", None]:
        return


class InGameState(IGameState):
    pass

    def update_logic(self,
                     events: list | None,
                     delta_ticks: int
                     ) -> Union["IGameState", None]:
        self.context.character_manager.update(delta_ticks)
        if events:
            for event in events:
                for eventkey in event.keys():
                    if eventkey == InGameEvents.PAUSE:
                        self.context.state = PauseMenuState(self.context)
        return None
