from src.PacMan.game_logic.collision import CollisionManager
from src.PacMan.game_logic.gamemanager.game_sm import (IGameState,
                                                       OpeningMenuState)
from src.PacMan.game_logic.maze.maze import Maze, MazeFactory
from src.PacMan.game_logic.characters.charactermng import CharacterManager
import time


class GameLogicManager:
    def __init__(self, nr_maze_cells: int, new_call_time: float) -> None:
        self.state: IGameState = OpeningMenuState()
        self.collision_mng = CollisionManager()
        self.maze: Maze = self._init_maze(nr_maze_cells)
        self.character_manager: CharacterManager = CharacterManager()
        self.call_time: float = new_call_time
        self.previous: float = 0
        # self.menu_manager:
        # self.time_manager:
        # self.player:

    def update_logic(self, events: list, new_call_time: float) -> IGameState:
        self.previous = self.call_time
        self.call_time = new_call_time
        delta_time = self.call_time - self.previous
        self.state.update_logic(delta_time)

    @staticmethod
    def _init_maze(nb_cells: int):
        return MazeFactory(nb_cells).make_maze()


if __name__ == '__main__':
    begin = time.time()
    gamelogicmanager = GameLogicManager(20, begin)
