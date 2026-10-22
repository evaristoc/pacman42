from src.PacMan.game_logic.characters.ghostsai import (AIStrategy,
                                                       BlinkyAI,
                                                       ClydeAI,
                                                       PinkyAI,
                                                       InkyAI)
from src.PacMan.game_logic.characters.ghostsm import (IGhostState,
                                                      ChasingGhostState)
from src.PacMan.game_logic.maze.maze import Maze

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

    def __init__(self, name: GhostName, maze: Maze) -> None:
        """Initializes a Ghost with a name, default state, and AI strategy.

        Args:
            name: The GhostName identity used to determine the AI and
            spawn point.
        """
        self.name: GhostName = name
        self.maze: Maze = maze
        self.spawn_point: tuple[int, int] = self._get_spawn_point()
        self.strategy: AIStrategy = self._get_ghost_ai(maze)
        self.position: tuple[int, int] = self.spawn_point
        self.old_position: tuple[int, int] = self.position
        self.state: IGhostState = ChasingGhostState(self.strategy)

    def update(self, *, delta_ticks: int, pacman_position: tuple[int, int]) -> None:
        """Updates the ghost's position and state based on game time.

        Args:
            delta_time: The time elapsed since the last update frame.
        """
        if pacman_position == self.position:
            return
        move, new_state = self.state.update(
            delta_ticks=delta_ticks,
            pacman_position=pacman_position,
            ghost_position=self.position
        )
        if new_state:
            self.state = new_state
        if move:
            self._process_move(move)
            print(f"{delta_ticks}: I'm {self.name.name}. My position is {self.position}. My previous position was {self.old_position}. My move was{move}. My state is {self.state.__class__.__name__}")
        if self.position == pacman_position:
            print(f"GOTCHAA from {self.name.name}")

    def get_position(self) -> tuple[float, float]:
        """Returns the current coordinates of the ghost.

        Returns:
            A tuple of (x, y) coordinates.
        """
        return self.position

    def big_pellet_activated(self) -> None:
        self.state = self.state.big_pellet_activated()

    def collide_with_pacman(self) -> None:
        """Handles the logic when the ghost collides with Pac-Man.

        Changes state to EATEN if the ghost is currently FRIGHTENED.

        Raises:
            GhostStateError: If the ghost is in an undefined state.
        """
        self.state.collide_with_pacman()

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
        dx, dy = move
        old_x, old_y = self.position
        new_position = (old_x + dx, old_y + dy)
        self.old_position = self.position
        self.position = new_position


class GhostManager:
    def __init__(self, maze: Maze) -> None:
        self.ghosts = {
            GhostName.BLINKY: Ghost(GhostName.BLINKY, maze),
            GhostName.CLYDE: Ghost(GhostName.CLYDE, maze),
            GhostName.INKY: Ghost(GhostName.INKY, maze),
            GhostName.PINKY: Ghost(GhostName.PINKY, maze)
        }

    def update(self, delta_ticks: int, 
               pacman_position: tuple[int, int]
               ) -> None:
        for ghost in self.ghosts.values():
            ghost.update(delta_ticks=delta_ticks,
                         pacman_position=pacman_position)
