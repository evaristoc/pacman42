from src.PacMan.game_logic.gamemanager.game_sm import IGameState, MainMenuState
from src.PacMan.validation_contracts.event_enums import IEventEnums
from src.PacMan.game_logic.gamemanager.gamesession import GameSession, GameSessionFactory
from src.PacMan.game_logic.player import Player
from src.PacMan.game_logic.score_mng import ScoreManager
from typing import Any
# for testing
from src.PacMan.game_logic.mock_observer import IObserver

MAX_LEVEL = 3


class GameLogicManager:
    def __init__(self) -> None:
        self.ticks: int = 0
        self.level: int = 1
        self.player = Player("anonymous")
        self.scoremng = ScoreManager(self.player)
        self.subscribers: list[IObserver] = []
        self.session: GameSession | None = None
        self.state: IGameState = MainMenuState(self)

    def update_logic(self,
                     events: dict[IEventEnums, dict[Any, Any] | None] | None
                     ) -> IGameState:
        self.ticks += 1
        print(f"ticks: {self.ticks}")
        self.state.subscribe()
        new_state = self.state.update_logic(events, self.ticks)
        if new_state:
            self.state = new_state
        return self.state

    def subscribe(self, subscriber: IObserver) -> None:
        self.subscribers.append(subscriber)

    def create_game_session(self) -> GameSession:
        return GameSessionFactory().create_game_new_game(self.level,
                                                         self.scoremng,
                                                         self.player)

    def toggle_impotent_ghosts(self) -> None:
        print("Ghosts would now have been impotent...")
        return

    def final_level(self) -> bool:
        if self.level == MAX_LEVEL:
            return True
        return False


def test() -> None:
    import random
    import time
    from src.PacMan.game_logic.gamemanager.game_sm import IGameState, InGameState, MainMenuState, HighScoreRegisterState, PauseMenuState
    from src.PacMan.game_logic.mock_observer import ObserverTemp
    from src.PacMan.validation_contracts.event_enums import (
        InGameEvents, MainMenuEvents, PauseMenuEvents, HighScoreMenuEvents, HighScoreRegisterEvents, CheatingMenuEvents)
    gamelogicmanager = GameLogicManager()
    observer = ObserverTemp()
    gamelogicmanager.subscribe(observer)
    steps = 200
    event: dict[IEventEnums, dict[str, Any] | None] | None = None
    gamelogicmanager.update_logic({MainMenuEvents.HIGHSCORES: None})
    gamelogicmanager.update_logic({HighScoreMenuEvents.RETURN: None})
    gamelogicmanager.update_logic({MainMenuEvents.CHEATING: None})
    gamelogicmanager.update_logic({CheatingMenuEvents.IMPOTENTGHOSTS: None})
    gamelogicmanager.update_logic({CheatingMenuEvents.RETURN: None})
    state = gamelogicmanager.update_logic({MainMenuEvents.START: None})
    while steps > 0:
        event = None
        if steps % 10 == 0 and steps < 170 and type(state) == InGameState:
            position = gamelogicmanager.session.pacman.new_position.get_position_from_tile()
            tile = gamelogicmanager.session.maze.return_tile_from_position(
                position=position)
            possible_moves = tile.get_open_walls()
            new_move = random.choice(possible_moves)
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
        state = gamelogicmanager.update_logic(event)
        if type(state) is HighScoreRegisterState:
            gamelogicmanager.update_logic(
                events={HighScoreRegisterEvents.REGISTER: {'name': "Dirky"}})
        time.sleep(0.3)
        steps -= 1


if __name__ == '__main__':
    test()