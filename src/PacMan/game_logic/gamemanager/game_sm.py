from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
from typing import Union

if TYPE_CHECKING:
    from src.PacMan.game_logic.gamemanager.gamelogicmng import GameLogicManager


class IGameState(ABC):
    def __init__(self, context: "GameLogicManager"):
        self.context: "GameLogicManager" = context

    @abstractmethod
    def update_logic(self,
                     events: list | None,
                     delta_ticks: int
                     ) -> Union["IGameState", None]:
        pass


class OpeningMenuState(IGameState):
    pass


class PlayingGameState(IGameState):
    pass

    def update_logic(self, events: list, delta_ticks: int):
        self.context.character_manager.update(delta_ticks)
