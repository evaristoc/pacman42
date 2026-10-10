from abc import ABC, abstractmethod
from .ghosts import GhostState
import random


class AIStrategy(ABC):
    def __init__(self, spawn_pos: tuple[float, float]):
        self.spawn_pos = spawn_pos

    @abstractmethod
    def decide_move(
        self,
        ghost_pos: tuple[float, float],
        pacman_pos: tuple[float, float],
        mode: GhostState
    ) -> tuple[float, float]:
        pass

    def _return_to_spawn(
        self,
        ghost_pos: tuple[float, float]
    ) -> tuple[float, float]:
        """All ghosts return to spawn the same way."""
        return self._pathfind_to(ghost_pos, self.spawn_pos)

    def _random_move(self) -> tuple[float, float]:
        """All ghosts flee randomly when frightened."""
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        return random.choice(directions)

    def _pathfind_to(
        self,
        start: tuple[float, float],
        target: tuple[float, float]
    ) -> tuple[float, float]:
        """A* or BFS pathfinding — shared by all ghosts."""
        # Generic pathfinding logic
        return (0, 0)  # TODO


class BlinkyAI(AIStrategy):
    """Chase directly at Pacman."""

    def decide_move(self, ghost_pos, pacman_pos, mode):
        pass


class PinkyAI(AIStrategy):
    """Aim 4 tiles ahead of Pacman."""

    def decide_move(self, ghost_pos, pacman_pos, mode):
        pass

    def _aim_ahead(self, pacman_pos, tiles: int):
        """Predict where Pacman will be."""
        pass


class InkyAI(AIStrategy):
    """Complex: use Blinky's position to triangulate."""

    def decide_move(self, ghost_pos, pacman_pos, mode):
        pass

    def _triangulate(self, pacman_pos, blinky_pos):
        """Inky-specific chase logic."""
        pass


class ClydeAI(AIStrategy):
    """Chase if far, else scatter."""

    def decide_move(self, ghost_pos, pacman_pos, mode):
        pass

    def _distance(self, pos1, pos2):
        pass
