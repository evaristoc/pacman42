from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
from src.PacMan.game_logic.ingame.characters.ghosts.ghostsai import AIStrategy
import time
from typing import Union

CHASING_GHOST_TICK_SPEED: int = 1
FRIGHTENED_GHOST_TICK_SPEED: int = 1

if TYPE_CHECKING:
    from src.PacMan.game_logic.ingame.characters.ghosts.ghosts import Ghost


class IGhostState(ABC):
    def __init__(self, context: "Ghost"):
        self.context: "Ghost" = context
        self.strategy: AIStrategy = self.context.strategy

    @abstractmethod
    def update(self, *,
               delta_ticks: int,
               pacman_position: tuple[int, int],
               pacman_direction: tuple[int, int],
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
    def __init__(self, context: "Ghost") -> None:
        super().__init__(context=context)
        self.tick_speed: int = self.context.speed
        self.frightened_timer: float = time.time() + 8

    def update(self, *,
               delta_ticks: int,
               pacman_position: tuple[int, int],
               pacman_direction: tuple[int, int],
               ghost_position: tuple[int, int]
               ) -> tuple[tuple[int, int] | None, Union[IGhostState, None]]:
        move = None
        if time.time() > self.frightened_timer:
            return None, ScatterGhostState(self.context)
        if delta_ticks % self.tick_speed == 0:
            move = self.strategy.decide_move(ghost_pos=ghost_position,
                                             pacman_direction=pacman_direction,
                                             pacman_pos=pacman_position)
        return move, None

    def big_pellet_activated(self) -> IGhostState:
        return FrightenedGhostState(self.context)

    def collide_with_pacman_does_ghost_die(self) -> tuple[Union["IGhostState", None], bool]:
        return None, False


class FrightenedGhostState(IGhostState):
    def __init__(self, context: "Ghost") -> None:
        super().__init__(context=context)
        self.frightened_timer: float = time.time() + 30
        self.tick_speed: int = self.context.speed

    def update(self, *,
               delta_ticks: int,
               pacman_position: tuple[int, int],
               pacman_direction: tuple[int, int],
               ghost_position: tuple[int, int]
               ) -> tuple[tuple[int, int] | None, Union[IGhostState, None]]:
        move = None
        if time.time() > self.frightened_timer:
            return None, ChasingGhostState(self.context)
        if delta_ticks % self.tick_speed == 0:
            move = self.strategy.random_move(ghost_position)
        return (move, None)

    def big_pellet_activated(self) -> IGhostState:
        return FrightenedGhostState(self.context)

    def collide_with_pacman_does_ghost_die(self) -> tuple[Union["IGhostState", None], bool]:
        return EatenGhostState(self.context), True


class EatenGhostState(IGhostState):
    def __init__(self, context: "Ghost") -> None:
        super().__init__(context=context)
        self.tick_speed = 5

    def update(self, *,
               delta_ticks: int,
               pacman_position: tuple[int, int],
               pacman_direction: tuple[int, int],
               ghost_position: tuple[int, int]
               ) -> tuple[tuple[int, int] | None, Union[IGhostState, None]]:
        move = None
        if ghost_position == self.context.spawn_point:
            return (None, ChasingGhostState(self.context))
        move = self.strategy.return_to_spawn(ghost_position)
        return move, None

    def big_pellet_activated(self) -> IGhostState:
        return self

    def collide_with_pacman_does_ghost_die(self) -> tuple[Union["IGhostState", None], bool]:
        return None, False


class ScatterGhostState(IGhostState):
    def __init__(self, context: "Ghost") -> None:
        super().__init__(context=context)
        self.frightened_timer: float = time.time() + 5

    def update(self, *,
               delta_ticks: int,
               pacman_position: tuple[int, int],
               pacman_direction: tuple[int, int],
               ghost_position: tuple[int, int]
               ) -> tuple[tuple[int, int] | None, Union[IGhostState, None]]:
        if time.time() > self.frightened_timer:
            return None, ChasingGhostState(self.context)
        if delta_ticks % self.context.speed == 0:
            move = self.strategy.return_to_spawn(ghost_pos=ghost_position)
            return (move, None)
        return None, None

    def big_pellet_activated(self) -> IGhostState:
        return FrightenedGhostState(self.context)

    def collide_with_pacman_does_ghost_die(self) -> tuple[Union["IGhostState", None], bool]:
        return None, False
