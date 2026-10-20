from src.PacMan.game_logic.characters.characterABC import GameCharacter
from src.PacMan.game_logic.maze.maze import Maze


class Pacman(GameCharacter):
    """Represents Pac-Man, the player-controlled character in the game.

    Pacman is responsible for tracking its own position and handling movement
    updates.

    The player controls Pacman's direction, and collision
    detection determines interactions with pellets, power-ups, and ghosts.
    """

    def __init__(self, maze: Maze) -> None:
        """Initialize Pac-Man at its spawn point.

        Sets up Pac-Man's initial position and prepares it for gameplay.
        """
        self.spawn_point = self._get_spawn_point()
        self.maze: Maze = maze

    def update(self, delta_ticks: int) -> None:
        """Update Pac-Man's state each frame.

        Handles movement based on player input, updates animation frames,
        manages power-up timers, and checks for collisions with game objects.

        Args:
            delta_time: The time elapsed since the last frame in seconds.
        """
        pass

    def get_position(self) -> tuple[int, int]:
        """Get Pac-Man's current position in world space.

        Returns:
            A tuple of (x, y) coordinates representing Pac-Man's current
            location.
        """
        return (0, 0)  # TODO

    def _get_spawn_point(self) -> tuple[float, float]:
        """Get Pac-Man's spawn point in world space.

        Returns the position where Pac-Man starts each game and where it
        respawns after losing a life.

        Returns:
            A tuple of (x, y) coordinates representing the spawn point
            location.
        """
        return (0, 0)  # TODO
