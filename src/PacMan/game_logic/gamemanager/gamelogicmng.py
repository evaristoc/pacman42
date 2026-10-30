from src.PacMan.game_logic.gamemanager.game_sm import IGameState, MainMenuState
from src.PacMan.game_logic.menu.menu import IMenu, MenuSnapshot
from src.PacMan.validation_contracts.event_enums import IEventEnums
from src.PacMan.game_logic.gamemanager.gamesession import GameSession, GameSessionFactory, GameSessionSnapshot
from src.PacMan.game_logic.player import Player, PlayerSnapshot
from src.PacMan.game_logic.score_mng import ScoreManager
from typing import Any
from dataclasses import dataclass

MAX_LEVEL = 3


@dataclass(frozen=True)
class GLMSnapshot:
    player: PlayerSnapshot
    game_state: str
    session: GameSessionSnapshot | None
    menu: MenuSnapshot | None


class GameLogicManager:
    def __init__(self, start_state: IGameState) -> None:
        self.ticks: int = 0
        self.player = Player("anonymous")
        self.scoremng = ScoreManager(self.player)
        self.session: GameSession | None = None
        self.menu: IMenu | None = None
        self.state: IGameState = start_state(self)

    def update_logic(self,
                     events: dict[IEventEnums, dict[Any, Any] | None] | None
                     ) -> None:
        self.ticks += 1
        new_state = self.state.update_logic(events, self.ticks)
        if new_state:
            self.state = new_state

    def view(self) -> "GLMSnapshot":
        if self.menu:
            menu_ss = self.menu.view()
        else:
            menu_ss = None
        if self.session:
            session_ss = self.session.view()
        else:
            session_ss = None

        return GLMSnapshot(player=self.player.view(),
                           game_state=self.state.__class__.__name__,
                           session=session_ss,
                           menu=menu_ss)

    def create_game_session(self) -> GameSession:
        return GameSessionFactory().create_game_new_game(self.player.level,
                                                         self.scoremng,
                                                         self.player)

    def toggle_impotent_ghosts(self) -> None:
        return

    def final_level(self) -> bool:
        if self.player.level == MAX_LEVEL:
            return True
        return False


def test() -> None:
    import random
    import time
    from src.PacMan.game_logic.gamemanager.game_sm import IGameState, InGameState, MainMenuState, HighScoreRegisterState, PauseMenuState
    from src.PacMan.validation_contracts.event_enums import (
        InGameEvents, MainMenuEvents, PauseMenuEvents, HighScoreMenuEvents, HighScoreRegisterEvents, CheatingMenuEvents)
    gamelogicmanager = GameLogicManager()
    steps = 200
    event: dict[IEventEnums, dict[str, Any] | None] | None = None
    gamelogicmanager.update_logic({MainMenuEvents.HIGHSCORES: None})
    gamelogicmanager.update_logic({HighScoreMenuEvents.RETURN: None})
    gamelogicmanager.update_logic({MainMenuEvents.CHEATING: None})
    gamelogicmanager.update_logic({CheatingMenuEvents.IMPOTENTGHOSTS: None})
    gamelogicmanager.update_logic({CheatingMenuEvents.RETURN: None})
    state = gamelogicmanager.update_logic({MainMenuEvents.START: None})
    snapshot = gamelogicmanager.view()
    while steps > 0:
        snapshot = gamelogicmanager.view()
        event = None
        if steps % 10 == 0 and steps < 190 and snapshot.game_state == "InGameState":
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
        gamelogicmanager.update_logic(event)
        snapshot = gamelogicmanager.view()
        time.sleep(0.3)
        steps -= 1


if __name__ == '__main__':
    test()
