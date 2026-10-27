from src.PacMan.game_logic.ingame.maze.maze import Maze
from src.PacMan.game_logic.ingame.maze.tile import Tile

PACMAN_TICK_SPEED = 10


class Pacman:
    """Represents Pac-Man, the player-controlled character in the game.

    Pacman is responsible for tracking its own position and handling movement
    updates.

    The player controls Pacman's direction, and collision
    detection determines interactions with pellets, power-ups, and ghosts.
    """

    def __init__(self, maze: Maze, speed: int) -> None:
        """Initialize Pac-Man at its spawn point.

        Sets up Pac-Man's initial position and prepares it for gameplay.
        """
        self.direction = (-1, 0)
        self.speed = speed
        self.maze: Maze = maze
        self.spawn_point = self._get_spawn_point()
        self.position: Tile = self.spawn_point
        self.old_position: Tile | None = None

    @property
    def direction(self) -> tuple[int, int]:
        return self._direction

    @direction.setter
    def direction(self,
                  new_direction: tuple[int, int]
                  ) -> None:
        if not isinstance(new_direction, tuple):
            raise ValueError("Direction must be a tuple")
        if len(new_direction) != 2:
            raise ValueError("Direction tuple must have exactly 2 elements")
        if not all(isinstance(x, int) for x in new_direction):
            raise ValueError("Direction tuple elements must be integers")
        if not all((x == 1 or x == -1 or x == 0) for x in new_direction):
            raise ValueError("Direction elements can only be 1 or -1.")
        if new_direction[0] != 0 and new_direction[1] != 0:
            raise ValueError("One of either direction elements"
                             " needs to be 0 always")
        if new_direction == (0, 0):
            raise ValueError("Direction cannot be (0, 0)")
        self._direction = new_direction

    def update(self, *,
               new_direction: tuple[int, int] | None,
               delta_ticks: int) -> None:
        if new_direction:
            self.direction = new_direction
        if delta_ticks % self.speed == 0:
            self.old_position = self.position
            self._process_move(self._direction)
            print(f"{delta_ticks}: I'm {self.__class__.__name__}. My position is {self.position.get_position_from_tile()}. My previous position was {self.old_position.get_position_from_tile()}. My attempted move was{self.direction}.")

    def _get_spawn_point(self) -> Tile:
        x_coordinate = (self.maze.width - 1) // 2
        y_coordinate = (self.maze.height - 1) - (self.maze.height // 5)
        return self.maze.return_tile_from_position(position=(x_coordinate,
                                                             y_coordinate))

    def _process_move(self, move: tuple[int, int]) -> None:
        valid_moves = self.position.get_open_walls()
        if move in valid_moves:
            dx, dy = move
            old_x = self.position.cell_position_x
            old_y = self.position.cell_position_y
            new_position = (old_x + dx, old_y + dy)
            self.position = self.maze.return_tile_from_position(
                position=new_position)
        else:
            return
