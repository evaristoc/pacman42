from abc import ABC, abstractmethod
from src.PacMan.game_logic.ingame.characters.ghosts.ghostsai import AIStrategy
import time
from typing import Union

CHASING_GHOST_TICK_SPEED: int = 1
FRIGHTENED_GHOST_TICK_SPEED: int = 1


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
    def collide_with_pacman_does_ghost_die(self) -> tuple[Union["IGhostState", None], bool]:
        pass


class ChasingGhostState(IGhostState):
    def __init__(self, strategy: AIStrategy, speed: int) -> None:
        super().__init__(strategy)
        self.tick_speed: int = speed

    def update(self, *,
               delta_ticks: int,
               pacman_position: tuple[int, int],
               ghost_position: tuple[int, int]
               ) -> tuple[tuple[int, int] | None, Union[IGhostState, None]]:
        move = None
        if delta_ticks % self.tick_speed == 0:
            move = self.strategy.decide_move(ghost_pos=ghost_position, 
                                             pacman_pos=pacman_position)
        return move, None

    def big_pellet_activated(self) -> IGhostState:
        return FrightenedGhostState(self.strategy, speed=self.tick_speed)

    def collide_with_pacman_does_ghost_die(self) -> tuple[Union["IGhostState", None], bool]:
        return None, False


class FrightenedGhostState(IGhostState):
    def __init__(self, strategy: AIStrategy, speed: int) -> None:
        super().__init__(strategy)
        self.frightened_timer: float = time.time() + 30
        self.tick_speed: int = speed

    def update(self, *,
               delta_ticks: int,
               pacman_position: tuple[int, int],
               ghost_position: tuple[int, int]
               ) -> tuple[tuple[int, int] | None, Union[IGhostState, None]]:
        move = None
        if time.time() > self.frightened_timer:
            return None, ChasingGhostState(self.strategy, self.tick_speed)
        if delta_ticks % self.tick_speed == 0:
            move = self.strategy.random_move(ghost_position)
        return (move, None)

    def big_pellet_activated(self) -> IGhostState:
        return FrightenedGhostState(self.strategy, self.tick_speed)

    def collide_with_pacman_does_ghost_die(self) -> tuple[Union["IGhostState", None], bool]:
        return EatenGhostState(self.strategy), True


class EatenGhostState(IGhostState):
    def __init__(self, strategy: AIStrategy) -> None:
        super().__init__(strategy)

    def update(self, *,
               delta_ticks: int,
               pacman_position: tuple[int, int],
               ghost_position: tuple[int, int]
               ) -> tuple[tuple[int, int] | None, Union[IGhostState, None]]:
        return None, None

    def big_pellet_activated(self) -> IGhostState:
        return self

    def collide_with_pacman_does_ghost_die(self) -> tuple[Union["IGhostState", None], bool]:
        return None, False


class ScatterGhostState(IGhostState):
    def __init__(self, strategy: AIStrategy) -> None:
        super().__init__(strategy)

    def update(self, *,
               delta_ticks: int,
               pacman_position: tuple[int, int],
               ghost_position: tuple[int, int]
               ) -> tuple[tuple[int, int] | None, Union[IGhostState, None]]:
        return None, None

    def big_pellet_activated(self) -> IGhostState:
        return self

    def collide_with_pacman_does_ghost_die(self) -> tuple[Union["IGhostState", None], bool]:
        return None, False
