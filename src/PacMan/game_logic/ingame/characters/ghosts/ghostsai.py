from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from src.PacMan.game_logic.ingame.maze.maze import Maze
from src.PacMan.game_logic.ingame.maze.tile import Tile
from src.PacMan.game_logic.ingame.characters.ghosts.a_star import AStar_next_move
import random

if TYPE_CHECKING:
    from src.PacMan.game_logic.ingame.characters.ghosts.ghosts import Ghost


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
        pacman_direction: tuple[int, int]
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

        return AStar_next_move(position=start, target=target, maze=self.maze)


class BlinkyAI(AIStrategy):
    """Chase directly at Pacman."""

    def decide_move(
        self, *,
        ghost_pos: tuple[int, int],
        pacman_pos: tuple[int, int],
        pacman_direction: tuple[int, int]
    ) -> tuple[int, int]:
        return AStar_next_move(position=ghost_pos, target=pacman_pos, maze=self.maze)


class PinkyAI(AIStrategy):
    """Aim 4 tiles ahead of Pacman."""

    def decide_move(
        self, *,
        ghost_pos: tuple[int, int],
        pacman_pos: tuple[int, int],
        pacman_direction: tuple[int, int]
    ) -> tuple[int, int]:
        target = self._aim_ahead(pacman_pos=pacman_pos,
                                 pacman_direction=pacman_direction)
        return AStar_next_move(position=ghost_pos, target=target, maze=self.maze)

    def _aim_ahead(self, pacman_pos: tuple[int, int], pacman_direction: tuple[int, int]) -> tuple[int, int]:
        """Predict where Pacman will be."""
        pos_x, pos_y = pacman_pos
        dir_x, dir_y = pacman_direction
        for x in range(3, -1, -1):
            temp_tile: Tile | None = self.maze.return_tile_from_position(
                position=((pos_x + (dir_x * x)), (pos_y + (dir_y * x))))
            if temp_tile:
                return temp_tile.get_position_from_tile()
        return pacman_pos


class InkyAI(AIStrategy):
    """Complex: use Blinky's position to triangulate."""

    def __init__(self, spawn_pos: tuple[int, int], maze: Maze, blinky: "Ghost") -> None:
        super().__init__(spawn_pos=spawn_pos, maze=maze)
        self.blinky = blinky

    def decide_move(
        self, *,
        ghost_pos: tuple[int, int],
        pacman_pos: tuple[int, int],
        pacman_direction: tuple[int, int]
    ) -> tuple[int, int]:
        target = self._triangulate(
            pacman_pos=pacman_pos, pacman_direction=pacman_direction)
        return AStar_next_move(position=ghost_pos, target=target, maze=self.maze)

    def _triangulate(self, pacman_pos: tuple[int, int], pacman_direction: tuple[int, int]) -> tuple[int, int]:
        """Inky-specific chase logic."""
        pos_x, pos_y = pacman_pos
        dir_x, dir_y = pacman_direction
        for x in range(3, -1, -1):
            temp_tile: Tile | None = self.maze.return_tile_from_position(
                position=((pos_x + (dir_x * x)), (pos_y + (dir_y * x))))
            if temp_tile:
                origin = temp_tile.get_position_from_tile()
                break
        blinky_pos = self.blinky.new_position.get_position_from_tile()
        vector_O_to_blinky = (
            (blinky_pos[0] - origin[0]), (blinky_pos[1] - origin[1]))

        negative_x = 1
        negative_y = 1
        if vector_O_to_blinky[0] < 0:
            negative_x = -1
        if vector_O_to_blinky[1] < 0:
            negative_y = -1

        for x in range(abs(vector_O_to_blinky[0]), -1, -1):
            for y in range(abs(vector_O_to_blinky[1]), -1, -1):
                new_target = ((origin[0] + (negative_x * x)),
                              (origin[1] + (negative_y * y)))
                temp_tile = self.maze.return_tile_from_position(
                    position=new_target)
                if temp_tile:
                    print("whooooowww")
                    return temp_tile.get_position_from_tile()
        return pacman_pos


class ClydeAI(AIStrategy):
    """Chase if far, else scatter."""

    def decide_move(
        self, *,
        ghost_pos: tuple[int, int],
        pacman_pos: tuple[int, int],
        pacman_direction: tuple[int, int]
    ) -> tuple[int, int]:
        distance = self._distance(ghost_pos, pacman_pos)
        if distance < 3:
            return self.return_to_spawn(ghost_pos=ghost_pos)
        else:
            return AStar_next_move(position=ghost_pos,
                                   target=pacman_pos,
                                   maze=self.maze)

    @staticmethod
    def _distance(pos1: tuple[int, int], pos2: tuple[int, int]) -> float:
        return ((pos1[0] - pos2[0])**2 + (pos1[1]-pos2[1])**2)**(1/2)
