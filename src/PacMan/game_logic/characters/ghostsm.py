from abc import ABC, abstractmethod
from src.PacMan.game_logic.characters.ghostsai import AIStrategy
import time
from typing import Union
FRIGHTENED_GHOST_TICK_SPEED: int = 10


class IGhostState(ABC):
    def __init__(self, strategy: AIStrategy):
        self.strategy: AIStrategy = strategy

    @abstractmethod
    def update(self, *,
               delta_ticks: int,
               pacman_position: tuple[int, int],
               ghost_position: tuple[int, int]
               ) -> tuple[tuple[int, int] | None, Union["IGhostState", None]]:
        pass

    @abstractmethod
    def big_pellet_activated(self) -> "IGhostState":
        pass

    @abstractmethod
    def collide_with_pacman(self) -> None:
        pass


class ChasingGhostState(IGhostState):
    def update(self, *,
               delta_ticks: int,
               pacman_position: tuple[int, int],
               ghost_position: tuple[int, int]
               ) -> tuple[tuple[int, int] | None, Union[IGhostState, None]]:
        return ((0, 0), self)

    def big_pellet_activated(self) -> IGhostState:
        return FrightenedGhostState(self.strategy)

    def collide_with_pacman(self) -> None:
        pass


class FrightenedGhostState(IGhostState):
    def __init__(self, strategy: AIStrategy) -> None:
        super().__init__(strategy)
        self.frightened_timer: float = time.time() + 500
        self.tick_speed: int = FRIGHTENED_GHOST_TICK_SPEED

    def update(self, *,
               delta_ticks: int,
               pacman_position: tuple[int, int],
               ghost_position: tuple[int, int]
               ) -> tuple[tuple[int, int] | None, Union[IGhostState, None]]:
        move = None
        if time.time() > self.frightened_timer:
            return None, ChasingGhostState(self.strategy)
        if delta_ticks % self.tick_speed == 0:
            move = self.strategy.random_move(ghost_position)
        return (move, None)

    def big_pellet_activated(self) -> IGhostState:
        return FrightenedGhostState(self.strategy)

    def collide_with_pacman(self) -> None:
        pass


class EatenGhostState(IGhostState):
    def big_pellet_activated(self) -> None:
        pass


class ScatterGhostState(IGhostState):
    def big_pellet_activated(self) -> None:
        pass
