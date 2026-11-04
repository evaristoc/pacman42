from src.PacMan.game_logic.gamemanager.game_sm import IGameState, InGameState
from src.PacMan.game_logic.menu.menu import IMenu, MenuSnapshot
from src.PacMan.validation_contracts.event_enums import IEventEnums
from src.PacMan.game_logic.gamemanager.gamesession import GameSession, GameSessionFactory, GameSessionSnapshot
from src.PacMan.game_logic.player import Player, PlayerSnapshot
from src.PacMan.game_logic.score_mng import ScoreManager
from src.PacMan.database.db_mng import DatabaseManager
from src.PacMan.game_logic.highscore import HighScoreSnapshot, db_highsc_to_snapshot
from typing import Any, Callable
from dataclasses import dataclass

MAX_LEVEL = 3


@dataclass(frozen=True)
class GLMSnapshot:
    player: PlayerSnapshot
    game_state: str
    session: GameSessionSnapshot | None
    menu: MenuSnapshot | None
    highscores: HighScoreSnapshot | None


class GameLogicManager:
    def __init__(self,
                 databasemng: DatabaseManager,
                 start_state: Callable[["GameLogicManager"],
                                       IGameState] = InGameState,
                 ) -> None:
        self.ticks: int = 0
        self.player = Player("anonymous")
        self.scoremng = ScoreManager(self.player)
        self.dbm: DatabaseManager = databasemng
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
                           menu=menu_ss,
                           highscores=self._get_hs_snapshot())

    def _get_hs_snapshot(self) -> HighScoreSnapshot | None:
        with self.dbm as db:
            highscores = db.get_high_scores()
        return db_highsc_to_snapshot(highscores=highscores)

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


def debug():
    from src.PacMan.database.db_mng import create_database_mng
    from src.PacMan.game_logic.gamemanager.game_sm import MainMenuState
    from src.PacMan.validation_contracts.event_enums import MainMenuEvents, HighScoreRegisterEvents
    import time

    dbm = create_database_mng()
    glm = GameLogicManager(dbm, start_state=MainMenuState)

    snapshot = glm.view()
    ###### GAME_LOOP #####
    for i in range(20):
        glm.update_logic(None)
        if i % 5 == 0:
            print(f"Current highscore: {snapshot.highscores}")
        time.sleep(0.3)


