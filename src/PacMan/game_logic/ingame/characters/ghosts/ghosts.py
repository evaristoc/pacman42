from src.PacMan.game_logic.ingame.characters.ghosts.ghostsai import (AIStrategy,
                                                                     BlinkyAI,
                                                                     ClydeAI,
                                                                     PinkyAI,
                                                                     InkyAI)
from src.PacMan.game_logic.ingame.characters.ghosts.ghostsm import (IGhostState,
                                                                    ChasingGhostState)
from src.PacMan.game_logic.ingame.maze.maze import Maze
from src.PacMan.game_logic.ingame.maze.tile import Tile
from dataclasses import dataclass

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


@dataclass(frozen=True)
class GhostSnapShot:
    state: str
    position: tuple[float, float]


class Ghost:
    """A ghost entity that pursues Pac-Man using a specific AI strategy."""

    def __init__(self, *,
                 name: GhostName,
                 maze: Maze,
                 speed: int,
                 ai_strategy: AIStrategy,
                 spawn_point: tuple[int, int]) -> None:
        """Initializes a Ghost with a name, default state, and AI strategy.

        Args:
            name: The GhostName identity used to determine the AI and
            spawn point.
        """
        self.name: GhostName = name
        self.maze: Maze = maze
        self.spawn_point: tuple[int, int] = spawn_point
        self.strategy: AIStrategy = ai_strategy
        self.new_position: Tile = self.maze.return_tile_from_position(
            position=self.spawn_point)
        self.old_position: Tile = self.maze.return_tile_from_position(
            position=self.spawn_point)
        self.interpolated_position: tuple[float,
                                          float] = self.old_position.get_position_from_tile()
        self.speed: int = speed
        self.state: IGhostState = ChasingGhostState(self)
        self.first_run = True

    def update(self, *, delta_ticks: int, pacman_position: tuple[int, int], pacman_direction: tuple[int, int]) -> None:
        """Updates the ghost's position and state based on game time.

        Args:
            delta_time: The time elapsed since the last update frame.
        """

        move, new_state = self.state.update(
            delta_ticks=delta_ticks,
            pacman_position=pacman_position,
            pacman_direction=pacman_direction,
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

        print(f"{delta_ticks}: I'm {self.name.name}. My interpolated position is {self.interpolated_position}. My new position will be {self.new_position.get_position_from_tile()}. My old position is {self.old_position.get_position_from_tile()}. My state is {self.state.__class__.__name__}")

    def view(self) -> GhostSnapShot:
        return GhostSnapShot(state=self.state.__class__.__name__,
                             position=self.interpolated_position)

    def big_pellet_activated(self) -> None:
        self.state = self.state.big_pellet_activated()

    def collide_with_pacman_and_does_ghost_die(self) -> bool:
        new_state, ghost_dies = self.state.collide_with_pacman_does_ghost_die()
        if new_state:
            self.state = new_state
        return ghost_dies

    def _process_move(self, move: tuple[int, int] | None) -> None:
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
            direction_x = (self.new_position.get_position_from_tile()[0] -
                           self.old_position.get_position_from_tile()[0])
            direction_y = (self.new_position.get_position_from_tile()[1] -
                           self.old_position.get_position_from_tile()[1])
            interpolated_x = direction_x * interpolation_amount
            interpolated_y = direction_y * interpolation_amount
            old_position_x, old_position_y = self.old_position.get_position_from_tile()

            self.interpolated_position = (
                old_position_x + interpolated_x,
                old_position_y + interpolated_y)
        else:
            self.interpolated_position = self.old_position.get_position_from_tile()


class GhostFactory:
    GHOSTS = [GhostName.BLINKY,
              GhostName.CLYDE,
              GhostName.INKY,
              GhostName.PINKY]

    GHOST_AI = {GhostName.BLINKY: BlinkyAI,
                GhostName.CLYDE: ClydeAI,
                GhostName.INKY: InkyAI,
                GhostName.PINKY: PinkyAI}

    def __init__(self, maze: Maze, speed: int):
        self.maze: Maze = maze
        self.speed: int = speed
        self.ghost_spawn = {GhostName.BLINKY: (0, 0),
                            GhostName.CLYDE: (self.maze.width - 1, 0),
                            GhostName.INKY: (self.maze.width - 1,
                                             self.maze.height - 1),
                            GhostName.PINKY: (0, self.maze.height - 1), }

    def create_ghosts(self) -> dict[GhostName, Ghost]:
        ghosts: dict[GhostName, Ghost] = {}
        for ghost in self.GHOSTS:
            if ghost == GhostName.INKY:

                new_ghost_spawn = self.ghost_spawn[ghost]
                new_ghost_ai = self.GHOST_AI[ghost](maze=self.maze,
                                                    spawn_pos=new_ghost_spawn,
                                                    blinky=ghosts[GhostName.BLINKY])
            else:
                new_ghost_spawn = self.ghost_spawn[ghost]
                new_ghost_ai = self.GHOST_AI[ghost](spawn_pos=new_ghost_spawn,
                                                    maze=self.maze)
            ghosts[ghost] = Ghost(name=ghost,
                                  maze=self.maze,
                                  speed=self.speed,
                                  ai_strategy=new_ghost_ai,
                                  spawn_point=new_ghost_spawn)
        return ghosts


@dataclass(frozen=True)
class GhostMngSnapshot:
    ghost_snapshots: dict[str, GhostSnapShot]


class GhostManager:
    def __init__(self, maze: Maze, speed: int) -> None:
        self.ghost_factory: GhostFactory = GhostFactory(maze, speed)
        self.ghosts: dict[GhostName,
                          Ghost] = self.ghost_factory.create_ghosts()

    def update(self, delta_ticks: int,
               pacman_position: tuple[int, int],
               pacman_direction: tuple[int, int]
               ) -> None:
        for ghost in self.ghosts.values():
            ghost.update(delta_ticks=delta_ticks,
                         pacman_position=pacman_position,
                         pacman_direction=pacman_direction)

    def view(self) -> GhostMngSnapshot:
        return GhostMngSnapshot(ghost_snapshots={ghost_name.name: ghost.view() for ghost_name, ghost in self.ghosts.items()})

    def big_pellet_activated(self) -> None:
        for ghost in self.ghosts.values():
            ghost.big_pellet_activated()


if __name__ == '__main__':
    from src.PacMan.game_logic.ingame.maze.maze import MazeFactory
    mf = MazeFactory(nb_cells=12)
    gm = GhostManager(maze=mf.make_maze(), speed=10)
    print(gm.view())
