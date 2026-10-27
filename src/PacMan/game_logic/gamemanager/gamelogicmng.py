from src.PacMan.game_logic.gamemanager.game_sm import IGameState, InGameState
from src.PacMan.validation_contracts.event_enums import (IEventEnums,
                                                         InGameEvents)
from src.PacMan.game_logic.gamemanager.gamesession import GameSession, GameSessionFactory
from src.PacMan.game_logic.player import Player
from src.PacMan.game_logic.score_mng import ScoreManager
from typing import Any
# for testing
from src.PacMan.game_logic.mock_observer import IObserver


class GameLogicManager:
    def __init__(self) -> None:
        self.ticks: int = 0
        self.level: int = 1
        self.player = Player("anonymous")
        self.scoremng = ScoreManager(self.player)
        self.subscribers: list = []
        self.session: GameSession | None = None
        self.state: IGameState = InGameState(self)

    def update_logic(self,
                     events: dict[IEventEnums, dict[str, Any] | None] | None
                     ) -> IGameState:
        self.ticks += 1
        self.state.subscribe()
        new_state = self.state.update_logic(events, self.ticks)
        if new_state:
            self.state = new_state
        return self.state

    def subscribe(self, subscriber: IObserver) -> None:
        self.subscribers.append(subscriber)

    def create_game_session(self) -> GameSession:
        return GameSessionFactory().create_game_new_game(self.level, self.scoremng)


def test() -> None:
    import random
    import time
    from src.PacMan.game_logic.mock_observer import ObserverTemp
    gamelogicmanager = GameLogicManager()
    observer = ObserverTemp()
    gamelogicmanager.subscribe(observer)
    steps = 300
    event: dict[IEventEnums, dict[str, Any] | None] | None = None
    while steps > 0:
        if steps % 5 == 0:
            if gamelogicmanager.session:
                position = gamelogicmanager.session.pacman.position.get_position_from_tile()
                prev_pos = gamelogicmanager.session.pacman.old_position
                tile = gamelogicmanager.session.maze.return_tile_from_position(
                    position=position)
                possible_moves = tile.get_open_walls()
                new_move = random.choice(possible_moves)
                if ((position[0] + new_move[0]), (position[1] + new_move[1])) == prev_pos and len(possible_moves) > 1:
                    exclude = new_move
                    new_move = random.choice(
                        [move for move in possible_moves if move != exclude])
                if new_move == 'n' or new_move == (0, -1):
                    event = {InGameEvents.PACMAN_NORTH: None}
                elif new_move == 'e' or new_move == (1, 0):
                    event = {InGameEvents.PACMAN_EAST: None}
                elif new_move == 's' or new_move == (0, 1):
                    event = {InGameEvents.PACMAN_SOUTH: None}
                elif new_move == 'w' or new_move == (-1, 0):
                    event = {InGameEvents.PACMAN_WEST: None}
                else:
                    event = None
        if steps == 10:
            gamelogicmanager.update_logic({InGameEvents.PAUSE: None})
        gamelogicmanager.update_logic(event)
        time.sleep(0.3)
        steps -= 1


if __name__ == '__main__':
    test()
