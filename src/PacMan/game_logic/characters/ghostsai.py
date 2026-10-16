from abc import ABC, abstractmethod
from .ghosts import GhostState
import random


class AIStrategy(ABC):
    """Abstract base class defining the behavior strategy for ghosts in
    Pac-Man.

    Each ghost subclass implements a unique decision-making algorithm
    (chase, ambush, etc.) while inheriting common utilities for pathfinding,
    fleeing, and returning to spawn.
    """

    def __init__(self, spawn_pos: tuple[float, float]):
        """Initialize a ghost strategy with its spawn position.

        Args:
            spawn_pos: The (x, y) coordinates where the ghost respawns when
            caught or when exiting frightened mode.
        """
        self.spawn_pos = spawn_pos

    @abstractmethod
    def decide_move(
        self,
        ghost_pos: tuple[float, float],
        pacman_pos: tuple[float, float],
        mode: GhostState
    ) -> tuple[float, float]:
        """Determine the next move for the ghost based on current game state.

        Subclasses implement their unique behavior here. Movement decisions
        should consider the ghost's current mode (chase, scatter, frightened)
        and may use pathfinding, evasion, or random movement strategies.

        Args:
            ghost_pos: The ghost's current (x, y) position.
            pacman_pos: Pac-Man's current (x, y) position.
            mode: The ghost's current behavioral state (chase, scatter,
            frightened, etc.).

        Returns:
            A direction vector (dx, dy) representing the next move.
        """
        pass

    def _return_to_spawn(
        self,
        ghost_pos: tuple[float, float]
    ) -> tuple[float, float]:
        """Calculate the next move for the ghost to return to its spawn
        position.

        All ghosts use the same pathfinding logic when returning to spawn,
        typically after being caught by Pac-Man or exiting frightened mode.

        Args:
            ghost_pos: The ghost's current (x, y) position.

        Returns:
            A direction vector (dx, dy) toward the spawn position.
        """
        return self._pathfind_to(ghost_pos, self.spawn_pos)

    def _random_move(self) -> tuple[float, float]:
        """Select a random direction for the ghost to move.

        Used when the ghost is in frightened mode, causing erratic,
        unpredictable movement to make the ghost vulnerable and
        easier to catch.

        Returns:
            A random direction vector: one of (1, 0), (-1, 0), (0, 1), or 
            (0, -1).
        """
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        return random.choice(directions)

    def _pathfind_to(
        self,
        start: tuple[float, float],
        target: tuple[float, float]
    ) -> tuple[float, float]:
        """Calculate the next move toward a target position using pathfinding.

        Uses A* or BFS to find the shortest path, accounting for maze walls and
        obstacles. This shared utility is used by multiple ghost strategies and
        by the spawn-return behavior.

        Args:
            start: The starting (x, y) position.
            target: The target (x, y) position to pathfind toward.

        Returns:
            A direction vector (dx, dy) representing the first step of the 
            path.
        """
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
