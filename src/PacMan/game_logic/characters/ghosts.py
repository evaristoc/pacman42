from src.PacMan.game_logic.characters.characterABC import GameCharacter
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


class Ghost(GameCharacter):
    """A ghost entity that pursues Pac-Man using a specific AI strategy."""

    def __init__(self, name: GhostName, maze: Maze) -> None:
        """Initializes a Ghost with a name, default state, and AI strategy.

        Args:
            name: The GhostName identity used to determine the AI and
            spawn point.
        """
        self.name: GhostName = name
        self.maze: Maze = maze
        self.state: IGhostState = ChasingGhostState(self)
        self.spawn_point: tuple[int, int] = self._get_spawn_point()
        self.strategy: AIStrategy = self._get_ghost_ai()
        self.position: tuple[int, int] = self.spawn_point

    def update(self, delta_ticks: int) -> None:
        """Updates the ghost's position and state based on game time.

        Args:
            delta_time: The time elapsed since the last update frame.
        """
        self.state.update(delta_ticks)
        print(f"I'm {self.name.name}. My position is {self.position}")

    def set_state(self, new_state: IGhostState) -> None:
        self.state = new_state

    def get_position(self) -> tuple[float, float]:
        """Returns the current coordinates of the ghost.

        Returns:
            A tuple of (x, y) coordinates.
        """
        return self.position

    def big_pellet_activated(self) -> None:
        self.state.big_pellet_activated()

    def collide_with_pacman(self) -> None:
        """Handles the logic when the ghost collides with Pac-Man.

        Changes state to EATEN if the ghost is currently FRIGHTENED.

        Raises:
            GhostStateError: If the ghost is in an undefined state.
        """
        self.state.collide_with_pacman()

    def _get_ghost_ai(self) -> AIStrategy:
        """Determines the AI strategy based on the ghost's name.

        Returns:
            An AIStrategy implementation specific to the ghost's identity.

        Raises:
            GhostError: If the ghost's name does not map to a known AI
            strategy.
        """
        match self.name:
            case GhostName.BLINKY:
                return BlinkyAI(self, self.spawn_point)
            case GhostName.CLYDE:
                return ClydeAI(self, self.spawn_point)
            case GhostName.INKY:
                return InkyAI(self, self.spawn_point)
            case GhostName.PINKY:
                return PinkyAI(self, self.spawn_point)
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
                return (1, 1)
            case GhostName.CLYDE:
                return (2, 2)
            case GhostName.INKY:
                return (3, 3)
            case GhostName.PINKY:
                return (4, 4)
            case _:
                raise GhostError("Stored invalid name in Ghost-object, "
                                 "so can't determine valid AIStrategy.")


class GhostManager:
    def __init__(self, maze: Maze) -> None:
        self.ghosts = {
            GhostName.BLINKY: Ghost(GhostName.BLINKY, maze),
            GhostName.CLYDE: Ghost(GhostName.CLYDE, maze),
            GhostName.INKY: Ghost(GhostName.INKY, maze),
            GhostName.PINKY: Ghost(GhostName.PINKY, maze)
        }

    def update(self):
        for ghost in self.ghosts.values:
            ghost.update()
