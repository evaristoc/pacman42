from src.PacMan.game_logic.collision import CollisionManager
from src.PacMan.game_logic.gamemanager.game_sm import (IGameState,
                                                       PlayingGameState)
from src.PacMan.game_logic.maze.maze import Maze, MazeFactory
from src.PacMan.game_logic.characters.charactermng import CharacterManager
from src.PacMan.game_logic.characters.ghosts import GhostName
from src.PacMan.validation_contracts.event_enums import IEventEnums
import time


class GameLogicManager:
    def __init__(self, nr_maze_cells: int) -> None:
        self.state: IGameState = PlayingGameState(self)
        self.collision_mng = CollisionManager()
        self.maze: Maze = self._init_maze(nr_maze_cells)
        self.character_manager: CharacterManager = CharacterManager(self.maze)
        self.ticks: int = 0

        # self.menu_manager:
        # self.time_manager:
        # self.player:

    def update_logic(self, events: list[dict[IEventEnums, list]] | None) -> IGameState:
        self.ticks += 1
        self.state.update_logic(events, self.ticks)
        return self.state

    @staticmethod
    def _init_maze(nb_cells: int) -> Maze:
        return MazeFactory(nb_cells=nb_cells).make_maze()


if __name__ == '__main__':
    gamelogicmanager = GameLogicManager(6)
    steps = 100
    while steps > 0:
        gamelogicmanager.update_logic(None)
        if steps == 18:
            gamelogicmanager.character_manager.ghost_mng.ghosts[GhostName.BLINKY].big_pellet_activated()
        steps -= 1

