from src.PacMan.game_logic.ingame.maze.maze import Maze, MazeFactory, MazeSnapshot
from src.PacMan.game_logic.ingame.time.time import TimeManager, TimeMngSnapshot
from src.PacMan.game_logic.ingame.time.time_sm import LevelActiveState
from src.PacMan.game_logic.ingame.characters.pacman import Pacman, PacmanSnapshot
from src.PacMan.game_logic.ingame.characters.ghosts.ghosts import GhostManager, GhostMngSnapshot
from src.PacMan.game_logic.ingame.collision import CollisionManager
from src.PacMan.game_logic.score_mng import ScoreManager
from src.PacMan.game_logic.player import Player
from src.PacMan.app_config.config import PACMAN_SPEED_PER_LVL, GHOST_SPEED_PER_LVL, MAZE_NR_CELLS, MAZE_SEED
from src.PacMan.game_logic.ingame.update_outcome import UpdateOutcome
from dataclasses import dataclass


@dataclass(frozen=True)
class GameSessionSnapshot:
    timemng: TimeMngSnapshot
    ghost_mng: GhostMngSnapshot
    pacman: PacmanSnapshot
    maze: MazeSnapshot


class GameSession:
    """
    The GameSession is responsible for holding the state of a single session.
    It contains the character manager, the time manager, the maze and the collision manager. 
    """

    def __init__(self, *, maze: Maze,
                 timemng: TimeManager,
                 pacman: Pacman,
                 ghostmng: GhostManager,
                 collisionmng: CollisionManager) -> None:
        self.timemng: TimeManager = timemng
        self.pacman: Pacman = pacman
        self.ghost_mng: GhostManager = ghostmng
        self.collision_mng: CollisionManager = collisionmng
        self.maze: Maze = maze

    def update(self, *,
               delta_ticks: int,
               pacman_move: tuple[int, int] | None = None
               ) -> UpdateOutcome:
        outcome = self.timemng.update()
        if outcome.value[0]:
            return outcome
        if type(self.timemng.state) is LevelActiveState:
            self.pacman.update(delta_ticks=delta_ticks,
                               new_direction=pacman_move)
            self.ghost_mng.update(delta_ticks,
                                  self.pacman.new_position.get_position_from_tile(),
                                  self.pacman.direction)
            outcome = self.collision_mng.update()
        return outcome

    def view(self) -> GameSessionSnapshot:
        maze_ss = self.maze.view()
        timemng_ss = self.timemng.view()
        ghost_mng_ss = self.ghost_mng.view()
        pacman_ss = self.pacman.view()
        return GameSessionSnapshot(pacman=pacman_ss,
                                   timemng=timemng_ss,
                                   ghost_mng=ghost_mng_ss,
                                   maze=maze_ss)


class GameSessionFactory:
    def create_game_new_game(self, level: int, scoremng: ScoreManager, player: Player, friendly_ghosts: bool) -> GameSession:
        if type(level) is not int:
            raise ValueError("level-variable is not an int.")
        if level not in MAZE_SEED.keys():
            raise ValueError(f"level-variable is invalid number: {level}")
        new_maze = MazeFactory(nb_cells=MAZE_NR_CELLS,
                               seed=MAZE_SEED[level]).make_maze()
        new_pacman = Pacman(new_maze, speed=PACMAN_SPEED_PER_LVL[level])
        new_timemng = TimeManager()
        new_ghostmng = GhostManager(
            new_maze, speed=GHOST_SPEED_PER_LVL[level])
        new_collisionmng = CollisionManager(maze=new_maze,
                                            pacman=new_pacman,
                                            ghostmng=new_ghostmng,
                                            timemng=new_timemng,
                                            player=player,
                                            scoremng=scoremng,
                                            friendly_ghosts=friendly_ghosts)
        return GameSession(maze=new_maze,
                           timemng=new_timemng,
                           pacman=new_pacman,
                           ghostmng=new_ghostmng,
                           collisionmng=new_collisionmng)
