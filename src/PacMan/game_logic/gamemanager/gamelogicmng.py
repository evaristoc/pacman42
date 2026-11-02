from src.PacMan.game_logic.gamemanager.game_sm import IGameState, InGameState
from src.PacMan.game_logic.menu.menu import IMenu, MenuSnapshot
from src.PacMan.validation_contracts.event_enums import IEventEnums
from src.PacMan.game_logic.gamemanager.gamesession import GameSession, GameSessionFactory, GameSessionSnapshot
from src.PacMan.game_logic.player import Player, PlayerSnapshot
from src.PacMan.game_logic.score_mng import ScoreManager
from typing import Any, Callable
from dataclasses import dataclass

MAX_LEVEL = 3


@dataclass(frozen=True)
class GLMSnapshot:
    player: PlayerSnapshot
    game_state: str
    session: GameSessionSnapshot | None
    menu: MenuSnapshot | None


class GameLogicManager:
    def __init__(self,
                 start_state: Callable[["GameLogicManager"], IGameState] = InGameState
                 ) -> None:
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

    def view(self) -> GLMSnapshot:
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