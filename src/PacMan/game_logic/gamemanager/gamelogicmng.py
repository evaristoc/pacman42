from src.PacMan.game_logic.collision import CollisionManager
from src.PacMan.game_logic.gamemanager.game_sm import (IGameState,
                                                       InGameState)
from src.PacMan.game_logic.maze.maze import Maze, MazeFactory
from src.PacMan.game_logic.characters.charactermng import CharacterManager
from src.PacMan.game_logic.characters.ghosts import GhostName
from src.PacMan.validation_contracts.event_enums import IEventEnums
from typing import Any
import time


class GameLogicManager:
    def __init__(self, nr_maze_cells: int) -> None:
        self.state: IGameState = InGameState(self)
        self.collision_mng = CollisionManager()
        self.maze: Maze = self._init_maze(nr_maze_cells)
        self.character_manager: CharacterManager = CharacterManager(self.maze)
        self.ticks: int = 0

        # self.menu_manager:
        # self.time_manager:
        # self.player:

    def update_logic(self,
                     events: dict[IEventEnums, dict[str, Any] | None] | None
                     ) -> IGameState:
        self.ticks += 1
        new_state = self.state.update_logic(events, self.ticks)
        if new_state:
            self.state = new_state
        return self.state

    @staticmethod
    def _init_maze(nb_cells: int) -> Maze:
        return MazeFactory(nb_cells=nb_cells).make_maze()


if __name__ == '__main__':
    from src.PacMan.validation_contracts.event_enums import InGameEvents
    gamelogicmanager = GameLogicManager(15)
    steps = 300
    event: dict[IEventEnums, dict[str, Any] | None] | None = None
    while steps > 0:
        gamelogicmanager.update_logic(event)
        if steps % 50 == 0:
            new_move = input()
            if new_move == 'n':
                event = {InGameEvents.PACMAN_NORTH: None}
            elif new_move == 'e':
                event = {InGameEvents.PACMAN_EAST: None}
            elif new_move == 's':
                event = {InGameEvents.PACMAN_SOUTH: None}
            elif new_move == 'w':
                event = {InGameEvents.PACMAN_WEST: None}
            else:
                event = None

        if steps == 10:
            gamelogicmanager.update_logic({InGameEvents.PAUSE: None})
        steps -= 1
