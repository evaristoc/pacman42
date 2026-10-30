from src.PacMan.game_logic.ingame.maze.maze import Maze, MazeFactory
from src.PacMan.game_logic.ingame.time.time import TimeManager
from src.PacMan.game_logic.ingame.characters.pacman import Pacman
from src.PacMan.game_logic.ingame.characters.ghosts.ghosts import GhostManager
from src.PacMan.game_logic.ingame.collision import CollisionManager
from src.PacMan.game_logic.score_mng import ScoreManager
from src.PacMan.game_logic.player import Player


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
        self.maze: Maze = maze
        self.timemng: TimeManager = timemng
        self.pacman: Pacman = pacman
        self.ghost_mng: GhostManager = ghostmng
        self.collision_mng: CollisionManager = collisionmng

    def update(self, *,
               delta_ticks: int,
               pacman_move: tuple[int, int] | None = None
               ) -> tuple[bool, bool | None]:
        game_over_and_level_won = self.timemng.update()
        if game_over_and_level_won[0]:
            return game_over_and_level_won
        if self.timemng.level_running:
            self.pacman.update(delta_ticks=delta_ticks,
                               new_direction=pacman_move)
            self.ghost_mng.update(delta_ticks,
                                  self.pacman.new_position.get_position_from_tile(),
                                  self.pacman.direction)
            game_over_and_level_won = self.collision_mng.update()
        return game_over_and_level_won


class GameSessionFactory:
    GHOST_SPEED_PER_LEVEL: dict[int, int] = {1: 10, 2: 10, 3: 6}
    PACMAN_SPEED_PER_LEVEL: dict[int, int] = {1: 7, 2: 10, 3: 10}
    MAZE_SIZENSEED_PER_LEVEL: dict[int, tuple[int, int]] = {
        1: (7, 80), 2: (9, 45), 3: (8, 50)}

    def create_game_new_game(self, level: int, scoremng: ScoreManager, player: Player) -> GameSession:
        if not isinstance(level, int):
            raise ValueError("level-variable is not an int.")
        if not level > 0 or not level < 10:
            raise ValueError(f"level-variable is invalid number: {level}")
        new_maze = MazeFactory(nb_cells=self.MAZE_SIZENSEED_PER_LEVEL[level][0],
                               seed=self.MAZE_SIZENSEED_PER_LEVEL[level][1]).make_maze()
        new_pacman = Pacman(new_maze, speed=self.PACMAN_SPEED_PER_LEVEL[level])
        new_timemng = TimeManager()
        new_ghostmng = GhostManager(
            new_maze, speed=self.GHOST_SPEED_PER_LEVEL[level])
        new_collisionmng = CollisionManager(maze=new_maze,
                                            pacman=new_pacman,
                                            ghostmng=new_ghostmng,
                                            timemng=new_timemng,
                                            player=player,
                                            scoremng=scoremng)
        return GameSession(maze=new_maze,
                           timemng=new_timemng,
                           pacman=new_pacman,
                           ghostmng=new_ghostmng,
                           collisionmng=new_collisionmng)
