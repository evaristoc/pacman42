from src.PacMan.game_logic.ingame.characters.ghosts.ghostsai import (AIStrategy,
                                                                     BlinkyAI,
                                                                     ClydeAI,
                                                                     PinkyAI,
                                                                     InkyAI)
from src.PacMan.game_logic.ingame.characters.ghosts.ghostsm import (IGhostState,
                                                                    ChasingGhostState)
from src.PacMan.game_logic.ingame.maze.maze import Maze
from src.PacMan.game_logic.ingame.maze.tile import Tile

from enum import Enum


class GhostName(Enum):
    """The unique identities of the ghosts."""
    BLINKY = 1
    PINKY = 2
    INKY = 3
    CLYDE = 4


class GhostError(Exception):
    """Base exception for ghost-related errors."""
    pass


class Ghost:
    """A ghost entity that pursues Pac-Man using a specific AI strategy."""

    def __init__(self, name: GhostName, maze: Maze, speed: int) -> None:
        """Initializes a Ghost with a name, default state, and AI strategy.

        Args:
            name: The GhostName identity used to determine the AI and
            spawn point.
        """
        self.name: GhostName = name
        self.maze: Maze = maze
        self.spawn_point: tuple[int, int] = self._get_spawn_point()
        self.strategy: AIStrategy = self._get_ghost_ai(maze)
        self.new_position: Tile = self.maze.return_tile_from_position(
            position=self.spawn_point)
        self.old_position: Tile = self.maze.return_tile_from_position(
            position=self.spawn_point)
        self.interpolated_position: tuple[float, float]
        self.speed: int = speed
        self.state: IGhostState = ChasingGhostState(self.strategy, speed=speed)
        self.first_run = True

    def update(self, *, delta_ticks: int, pacman_position: tuple[int, int]) -> None:
        """Updates the ghost's position and state based on game time.

        Args:
            delta_time: The time elapsed since the last update frame.
        """

        move, new_state = self.state.update(
            delta_ticks=delta_ticks,
            pacman_position=pacman_position,
            ghost_position=self.new_position.get_position_from_tile(),

        )
        if new_state:
            self.state = new_state
        if move or self.first_run:
            self.old_position = self.new_position
            self.first_run = False
            self._process_move(move)
            self.interpolated_position = self.old_position.get_position_from_tile()
        else:
            self._move_interpolate(delta_ticks=delta_ticks)

        print(f"{delta_ticks}: I'm {self.name.name}. My interpolated position is {self.interpolated_position}. My new position will be {self.new_position.get_position_from_tile()}. My old position is {self.old_position.get_position_from_tile()}.")

    def big_pellet_activated(self) -> None:
        self.state = self.state.big_pellet_activated()

    def collide_with_pacman_and_does_ghost_die(self) -> bool:
        new_state, ghost_dies = self.state.collide_with_pacman_does_ghost_die()
        if new_state:
            self.state = new_state
        return ghost_dies

    def _get_ghost_ai(self, maze: Maze) -> AIStrategy:
        """Determines the AI strategy based on the ghost's name.

        Returns:
            An AIStrategy implementation specific to the ghost's identity.

        Raises:
            GhostError: If the ghost's name does not map to a known AI
            strategy.
        """
        match self.name:
            case GhostName.BLINKY:
                return BlinkyAI(self.spawn_point, maze)
            case GhostName.CLYDE:
                return ClydeAI(self.spawn_point, maze)
            case GhostName.INKY:
                return InkyAI(self.spawn_point, maze)
            case GhostName.PINKY:
                return PinkyAI(self.spawn_point, maze)
            case _:
                raise GhostError("Stored invalid name in Ghost-object, "
                                 "so can't determine valid AIStrategy.")

    def _get_spawn_point(self) -> tuple[int, int]:
        """Returns the default starting coordinates for the specific ghost.

        Returns:
            A tuple of (x, y) coordinates.

        Raises:
            GhostError: If the ghost's name is invalid.
        """  # TODO
        match self.name:
            case GhostName.BLINKY:
                return (0, 0)
            case GhostName.CLYDE:
                return (self.maze.width - 1, 0)
            case GhostName.INKY:
                return (self.maze.width - 1,  self.maze.height - 1)
            case GhostName.PINKY:
                return (0, self.maze.height - 1)
            case _:
                raise GhostError("Stored invalid name in Ghost-object, "
                                 "so can't determine valid AIStrategy.")

    def _process_move(self, move: tuple[int, int]) -> None:
        if not move:
            move = (0, 0)
        dx, dy = move
        old_x = self.old_position.cell_position_x
        old_y = self.old_position.cell_position_y
        new_position = (old_x + dx, old_y + dy)
        self.new_position = self.maze.return_tile_from_position(
            position=new_position)

    def _move_interpolate(self, delta_ticks: int) -> None:
        if not self.old_position == self.new_position:
            interpolation_amount = (delta_ticks %
                                    self.speed) * (1 / self.speed)
            direction_x = self.new_position.get_position_from_tile(
            )[0] - self.old_position.get_position_from_tile()[0]
            direction_y = self.new_position.get_position_from_tile(
            )[1] - self.old_position.get_position_from_tile()[1]
            interpolated_x = direction_x * interpolation_amount
            interpolated_y = direction_y * interpolation_amount
            old_position_x, old_position_y = self.old_position.get_position_from_tile()

            self.interpolated_position = (
                old_position_x + interpolated_x,
                old_position_y + interpolated_y)
        else:
            self.interpolated_position = self.old_position.get_position_from_tile()


class GhostManager:
    def __init__(self, maze: Maze, speed: int) -> None:
        self.ghosts = {
            GhostName.BLINKY: Ghost(GhostName.BLINKY, maze, speed),
            GhostName.CLYDE: Ghost(GhostName.CLYDE, maze, speed),
            GhostName.INKY: Ghost(GhostName.INKY, maze, speed),
            GhostName.PINKY: Ghost(GhostName.PINKY, maze, speed)
        }

    def update(self, delta_ticks: int,
               pacman_position: tuple[int, int]
               ) -> None:
        for ghost in self.ghosts.values():
            ghost.update(delta_ticks=delta_ticks,
                         pacman_position=pacman_position)

    def big_pellet_activated(self) -> None:
        for ghost in self.ghosts.values():
            ghost.big_pellet_activated()
