from src.PacMan.game_logic.characters.characterABC import GameCharacter
from src.PacMan.game_logic.characters.ghostsai import (AIStrategy,
                                                       BlinkyAI,
                                                       ClydeAI,
                                                       PinkyAI,
                                                       InkyAI)
from enum import Enum


class GhostState(Enum):
    """Defines the behavioral state of a ghost."""
    CHASING = 1
    FRIGHTENED = 2
    EATEN = 3


class GhostName(Enum):
    """The unique identities of the ghosts."""
    BLINKY = 1
    PINKY = 2
    INKY = 3
    CLYDE = 4


class GhostError(Exception):
    """Base exception for ghost-related errors."""
    pass


class GhostStateError(GhostError):
    """Exception raised when a ghost enters an invalid or undefined state."""
    pass


class Ghost(GameCharacter):
    """A ghost entity that pursues Pac-Man using a specific AI strategy."""

    def __init__(self, name: GhostName) -> None:
        """Initializes a Ghost with a name, default state, and AI strategy.

        Args:
            name: The GhostName identity used to determine the AI and
            spawn point.
        """
        self.name: GhostName = name
        self.state: GhostState = GhostState.CHASING
        self.spawn_point: tuple[float, float] = self._get_spawn_point()
        self.strategy: AIStrategy = self._get_ghost_ai()
        self.position: tuple[float, float] = self.spawn_point

    def update(self, delta_time: float) -> None:
        """Updates the ghost's position and state based on game time.

        Args:
            delta_time: The time elapsed since the last update frame.
        """
        pass

    def render(self) -> None:
        """Draws the ghost on the screen."""
        pass

    def get_position(self) -> tuple[float, float]:
        """Returns the current coordinates of the ghost.

        Returns:
            A tuple of (x, y) coordinates.
        """
        return (0, 0)  # TODO

    def become_frightened(self) -> None:
        """Transitions the ghost into the FRIGHTENED state."""
        pass

    def collide_with_pacman(self) -> None:
        """Handles the logic when the ghost collides with Pac-Man.

        Changes state to EATEN if the ghost is currently FRIGHTENED.

        Raises:
            GhostStateError: If the ghost is in an undefined state.
        """
        match self.state:
            case GhostState.CHASING:
                return
            case GhostState.FRIGHTENED:
                self.state = GhostState.EATEN
                return
            case GhostState.EATEN:
                return
            case _:
                raise GhostStateError("Somehow self.state inside a Ghost"
                                      "-object was an invalid state.")

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
                return BlinkyAI(self.spawn_point)
            case GhostName.CLYDE:
                return ClydeAI(self.spawn_point)
            case GhostName.INKY:
                return InkyAI(self.spawn_point)
            case GhostName.PINKY:
                return PinkyAI(self.spawn_point)
            case _:
                raise GhostError("Stored invalid name in Ghost-object, "
                                 "so can't determine valid AIStrategy.")

    def _get_spawn_point(self) -> tuple[float, float]:
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
                return (0, 0)
            case GhostName.INKY:
                return (0, 0)
            case GhostName.PINKY:
                return (0, 0)
            case _:
                raise GhostError("Stored invalid name in Ghost-object, "
                                 "so can't determine valid AIStrategy.")
