from src.PacMan.game_logic.collision import CollisionManager
from src.PacMan.game_logic.gamemanager.game_sm import (IGameState,
                                                       OpeningMenuState,
                                                       PlayingGameState)
from src.PacMan.game_logic.maze.maze import Maze, MazeFactory
from src.PacMan.game_logic.characters.charactermng import CharacterManager
from src.PacMan.game_logic.characters.ghosts import GhostName
import time


class GameLogicManager:
    def __init__(self, nr_maze_cells: int) -> None:
        self.state: IGameState = PlayingGameState(self)
        self.collision_mng = CollisionManager()
        self.maze: Maze = self._init_maze(nr_maze_cells)
        self.character_manager: CharacterManager = CharacterManager(self.maze)

        # self.menu_manager:
        # self.time_manager:
        # self.player:

    def update_logic(self, events: list, ticks: int) -> IGameState:
        self.state.update_logic(ticks)
        return self.state

    @staticmethod
    def _init_maze(nb_cells: int):
        return MazeFactory(nb_cells).make_maze()


if __name__ == '__main__':
    gamelogicmanager = GameLogicManager(20)
    steps = 20
    while steps > 0:
        gamelogicmanager.update_logic()
        if steps == 18:
            gamelogicmanager.character_manager.ghost_mng.ghosts[GhostName.BLINKY].big_pellet_activated()
        steps -= 1

