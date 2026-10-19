from abc import ABC, abstractmethod
from src.PacMan.game_logic.characters.ghosts import Ghost
import time

FRIGHTENED_GHOST_TICK_SPEED: int = 40


class IGhostState(ABC):
    def __init__(self, context: Ghost):
        self.context = context

    @abstractmethod
    def update(self, delta_ticks: int) -> None:
        pass

    @abstractmethod
    def big_pellet_activated(self) -> None:
        pass

    @abstractmethod
    def collide_with_pacman(self) -> None:
        pass


class ChasingGhostState(IGhostState):
    def __init__(self, context: Ghost) -> None:
        super().__init__(context)

    def update(self, delta_ticks: int) -> None:
        pass

    def big_pellet_activated(self) -> None:
        self.context.set_state(FrightenedGhostState(self.context))

    def collide_with_pacman(self) -> None:
        pass


class FrightenedGhostState(IGhostState):
    def __init__(self, context: Ghost) -> None:
        super().__init__(context)
        self.frightened_timer: float = time.time() + 90
        self.tick_speed: int = FRIGHTENED_GHOST_TICK_SPEED

    def update(self, delta_ticks: int) -> None:
        if time.time() > self.frightened_timer:
            self.context.set_state(ChasingGhostState(self.context))
            return
        if delta_ticks % self.tick_speed == 0:
            self.context.position = self.context.strategy.random_move()

    def big_pellet_activated(self) -> None:
        self.context.set_state(FrightenedGhostState(self.context))

    def collide_with_pacman(self) -> None:
        pass


class EatenGhostState(IGhostState):
    def big_pellet_activated(self) -> None:
        pass


class ScatterGhostState(IGhostState):
    def big_pellet_activated(self) -> None:
        pass
