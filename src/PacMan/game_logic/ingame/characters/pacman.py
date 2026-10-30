from src.PacMan.game_logic.ingame.maze.maze import Maze
from src.PacMan.game_logic.ingame.maze.tile import Tile
from dataclasses import dataclass

PACMAN_TICK_SPEED = 10

@dataclass(frozen=True)
class PacmanSnapshot:
    direction: tuple[float, float]
    position: tuple[float, float]

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
        self.new_direction: tuple[int, int] | None = None
        self.speed = speed
        self.maze: Maze = maze
        self.spawn_point = self._get_spawn_point()
        self.interpolated_position: tuple[float, float] = self.spawn_point.get_position_from_tile()
        self.new_position: Tile = None
        self.old_position: Tile = self.spawn_point
        self.first_run: bool = True

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
            self.new_direction = new_direction
        if delta_ticks % self.speed == 0 or self.first_run:
            if not self.first_run:
                self.old_position = self.new_position
            self.first_run = False
            if self.new_direction:
                self.direction = self.new_direction
            self._process_move(self._direction)
            self.interpolated_position = self.old_position.get_position_from_tile()
        else:
            self._move_interpolate(delta_ticks=delta_ticks)
        print(f"{delta_ticks}: I'm {self.__class__.__name__}. My interpolated position is {self.interpolated_position}. My new position will be {self.new_position.get_position_from_tile()}. My old position is {self.old_position.get_position_from_tile()}. My direction is {self.direction}")

    def view(self) -> PacmanSnapshot:
        return PacmanSnapshot(direction=self.direction, position=self.interpolated_position)
    
    def _get_spawn_point(self) -> Tile:
        x_coordinate = (self.maze.width - 1) // 2
        y_coordinate = (self.maze.height - 1) - (self.maze.height // 5)
        return self.maze.return_tile_from_position(position=(x_coordinate,
                                                             y_coordinate))

    def _move_interpolate(self, delta_ticks: int) -> None:
        if not self.old_position == self.new_position:
            interpolation_amount = (delta_ticks % self.speed) * (1 / self.speed)
            direction_x = self.new_position.get_position_from_tile()[0] - self.old_position.get_position_from_tile()[0]
            direction_y = self.new_position.get_position_from_tile()[1] - self.old_position.get_position_from_tile()[1]
            if direction_x > 1 or direction_y > 1:
                raise ValueError("Direction can never be more than 1.")
            interpolated_x = direction_x * interpolation_amount
            interpolated_y = direction_y * interpolation_amount
            old_position_x, old_position_y = self.old_position.get_position_from_tile()

            self.interpolated_position = (old_position_x + interpolated_x, old_position_y + interpolated_y)
        else:
            self.interpolated_position = self.old_position.get_position_from_tile()

    def _process_move(self, move: tuple[int, int]) -> None:
        valid_moves = self.old_position.get_open_walls()
        if move in valid_moves:
            dx, dy = move
            old_x = self.old_position.cell_position_x
            old_y = self.old_position.cell_position_y
            new_position = (old_x + dx, old_y + dy)
            self.new_position = self.maze.return_tile_from_position(
                position=new_position)
        else:
            self.new_position = self.old_position

    def pacman_dies(self) -> None:
        self.new_position = self.spawn_point
        self.old_position = self.spawn_point
        print(
            f"I'm Pacman. I died and am now at {self.new_position.get_position_from_tile()}.")
