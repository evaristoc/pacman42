from abc import ABC, abstractmethod
from src.PacMan.game_logic.maze.maze import Maze
from src.PacMan.game_logic.maze.tile import Tile
from src.PacMan.game_logic.characters.a_star import AStar_next_move
import random


class AIStrategy(ABC):
    """Abstract base class defining the behavior strategy for ghosts in
    Pac-Man.

    Each ghost subclass implements a unique decision-making algorithm
    (chase, ambush, etc.) while inheriting common utilities for pathfinding,
    fleeing, and returning to spawn.
    """

    def __init__(self, spawn_pos: tuple[int, int], maze: Maze) -> None:
        self.maze: Maze = maze
        self.spawn_pos: tuple[int, int] = spawn_pos

    @abstractmethod
    def decide_move(
        self, *,
        ghost_pos: tuple[int, int],
        pacman_pos: tuple[int, int],
    ) -> tuple[int, int]:
        pass

    def return_to_spawn(
        self,
        ghost_pos: tuple[int, int]
    ) -> tuple[int, int]:
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

    def random_move(self, ghost_pos: tuple[int, int]) -> tuple[int, int]:
        """Select a random direction for the ghost to move.

        Used when the ghost is in frightened mode, causing erratic,
        unpredictable movement to make the ghost vulnerable and
        easier to catch.

        Returns:
            A random direction vector: one of (1, 0), (-1, 0), (0, 1), or 
            (0, -1).
        """
        temp_tile = self.maze.grid[ghost_pos[1]][ghost_pos[0]]
        if isinstance(temp_tile, Tile):
            possible_directions = temp_tile.get_open_walls()
        else:
            raise ValueError("Getting a tile from the maze failed.")
        return random.choice(possible_directions)

    def _pathfind_to(
        self,
        start: tuple[int, int],
        target: tuple[int, int]
    ) -> tuple[int, int]:
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


        return (0, 0)  # TODO


class BlinkyAI(AIStrategy):
    """Chase directly at Pacman."""

    def decide_move(
        self, *,
        ghost_pos: tuple[int, int],
        pacman_pos: tuple[int, int],
    ) -> tuple[int, int]:
        return AStar_next_move(position=ghost_pos, target=pacman_pos, maze=self.maze)


class PinkyAI(AIStrategy):
    """Aim 4 tiles ahead of Pacman."""

    def decide_move(
        self, *,
        ghost_pos: tuple[int, int],
        pacman_pos: tuple[int, int],
    ) -> tuple[int, int]:
        return AStar_next_move(position=ghost_pos, target=pacman_pos, maze=self.maze)

    def _aim_ahead(self, pacman_pos, tiles: int):
        """Predict where Pacman will be."""
        pass


class InkyAI(AIStrategy):
    """Complex: use Blinky's position to triangulate."""

    def decide_move(
        self, *,
        ghost_pos: tuple[int, int],
        pacman_pos: tuple[int, int],
    ) -> tuple[int, int]:
        return AStar_next_move(position=ghost_pos, target=pacman_pos, maze=self.maze)
        pass

    def _triangulate(self, pacman_pos, blinky_pos):
        """Inky-specific chase logic."""
        pass


class ClydeAI(AIStrategy):
    """Chase if far, else scatter."""

    def decide_move(
        self, *,
        ghost_pos: tuple[int, int],
        pacman_pos: tuple[int, int],
    ) -> tuple[int, int]:
        return AStar_next_move(position=ghost_pos, target=pacman_pos, maze=self.maze)

    def _distance(self, pos1, pos2):
        pass
