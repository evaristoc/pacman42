from src.PacMan.game_logic.ingame.maze.maze import Maze, MazeFactory
from src.PacMan.game_logic.ingame.time.time import TimeManager


class GameSessionFactory:
    def __init__(self)
        self.mazefactory = MazeFactory()
        self.ghost_speed_per_lvl
        self.pacman_speed_per_lvl
        

class GameSession:
    """
    The GameSession is responsible for holding the state of a single session.
    It contains the character manager, the time manager, the maze and the collision manager. 
    """
    def __init__(self, maze: list[list[int]], charactermng, timemng: timemng)
        self.maze = maze
        self.charactermng = charactermng
        self.timemng = timemng
        self.pacman: Pacman = Pacman(maze)
        self.ghost_mng: GhostManager = GhostManager(maze)

    def update(self, *,
               delta_ticks: int,
               pacman_move: tuple[int, int] | None = None
               ) -> None:
        self.pacman.update(delta_ticks=delta_ticks,
                           new_direction=pacman_move)
        self.ghost_mng.update(delta_ticks, self.pacman.get_position())