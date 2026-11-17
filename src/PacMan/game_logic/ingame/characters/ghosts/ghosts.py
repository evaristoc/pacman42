from src.PacMan.game_logic.ingame.characters.ghosts.ghostsai import (
    AIStrategy,
    BlinkyAI,
    ClydeAI,
    PinkyAI,
    InkyAI)
from src.PacMan.game_logic.ingame.characters.ghosts.ghostsm import (
    IGhostState,
    ChasingGhostState,
    FrightenedGhostState,
    GhostCollision)
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
    interpolation: tuple[float, float]
    position_coordinate: tuple[float, float]
    previous_tile: Tile
    next_tile: Tile


class Ghost:
    """A ghost entity that pursues Pac-Man using a specific AI strategy."""

    def __init__(self, *,
                 name: GhostName,
                 maze: Maze,
                 speed: int,
                 ai_strategy: AIStrategy,
                 start_state: type[IGhostState] = ChasingGhostState,
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
        self.new_position: Tile = (self
                                   .maze
                                   .return_tile_from_pos_with_validation(
                                       position=self.spawn_point))
        self.old_position: Tile = (self
                                   .maze
                                   .return_tile_from_pos_with_validation(
                                       position=self.spawn_point))
        self.interpolated_position: tuple[float,
                                          float] = (self
                                                    .old_position
                                                    .get_position_from_tile())
        self.interpolation: tuple[float, float] = (0, 0)
        self.normal_speed: int = speed
        self.speed: int = self.normal_speed
        self.state: IGhostState = start_state(self)
        self.first_run = True

    def update(self, *,
               delta_ticks: int,
               pacman_position: tuple[int, int],
               pacman_direction: tuple[int, int]
               ) -> None:
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
            self.interpolated_position = (self
                                          .old_position
                                          .get_position_from_tile())
            self.interpolation = (0, 0)
        else:
            self._move_interpolate(delta_ticks=delta_ticks)

    def view(self) -> GhostSnapShot:
        return GhostSnapShot(state=self.state.__class__.__name__,
                             interpolation=self.interpolation,
                             position_coordinate=self.interpolated_position,
                             previous_tile=self.old_position,
                             next_tile=self.new_position)

    def big_pellet_activated(self) -> None:
        self.state = self.state.big_pellet_activated()

    def collide_with_pacman_and_does_ghost_die(self) -> GhostCollision:
        new_state, ghost_dies = self.state.collide_with_pacman_does_ghost_die()
        if new_state:
            self.state = new_state
        return ghost_dies

    def pacman_dies_reset(self) -> None:
        self.new_position = self.maze.return_tile_from_pos_with_validation(
            position=self.spawn_point)
        self.old_position = self.maze.return_tile_from_pos_with_validation(
            position=self.spawn_point)
        self.interpolated_position = self.old_position.get_position_from_tile()
        self.interpolation = (0, 0)

    def _process_move(self, move: tuple[int, int] | None) -> None:
        if not move:
            move = (0, 0)
        dx, dy = move
        old_x = self.old_position.cell_position_x
        old_y = self.old_position.cell_position_y
        new_position = (old_x + dx, old_y + dy)
        new_tile = self.maze.return_tile_from_pos_with_validation(
            position=new_position)
        self.new_position = new_tile

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
            self.interpolation = (interpolated_x, interpolated_y)
            old_position_x, old_position_y = (self
                                              .old_position
                                              .get_position_from_tile())

            self.interpolated_position = (
                old_position_x + interpolated_x,
                old_position_y + interpolated_y)
        else:
            self.interpolated_position = (self
                                          .old_position
                                          .get_position_from_tile())


class GhostFactory:
    GHOSTS = [GhostName.BLINKY,
              GhostName.CLYDE,
              GhostName.INKY,
              GhostName.PINKY]

    GHOST_AI: dict[GhostName, type[AIStrategy]] = {GhostName.BLINKY: BlinkyAI,
                                                   GhostName.CLYDE: ClydeAI,
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
            new_ghost_spawn = self.ghost_spawn[ghost]
            if ghost == GhostName.INKY:
                inky_strat = InkyAI(spawn_pos=new_ghost_spawn,
                                    maze=self.maze,
                                    blinky=ghosts[GhostName.BLINKY])
                new_ghost_ai: AIStrategy = inky_strat
            else:
                new_ghost_ai = self.GHOST_AI[ghost](spawn_pos=new_ghost_spawn,
                                                    maze=self.maze)
            ghosts[ghost] = Ghost(name=ghost,
                                  maze=self.maze,
                                  speed=self.speed,
                                  ai_strategy=new_ghost_ai,
                                  start_state=FrightenedGhostState,
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
        return GhostMngSnapshot(ghost_snapshots=({ghost_name.name:
                                                  ghost.view()
                                                  for ghost_name, ghost
                                                  in self.ghosts.items()}))

    def big_pellet_activated(self) -> None:
        for ghost in self.ghosts.values():
            ghost.big_pellet_activated()

    def reset(self) -> None:
        for ghost in self.ghosts.values():
            ghost.pacman_dies_reset()
