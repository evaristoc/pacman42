import logging
from pathlib import Path
from src.PacMan.validation_contracts.valid_game_config import ValidBoardConfig
from src.PacMan.renderer.assets import ImgsAsset
from src.PacMan.renderer.strategies.imgs_loading_strategies import ConfiguratorT
from src.PacMan.database.db_mng import DatabaseManager
from src.PacMan.game_logic.gamemanager.gamelogicmng import GameLogicManager
from src.PacMan.renderer.renderer_engine import PyGMiniLibXEmulator
from src.PacMan.game_logic.gamemanager.game_sm import IGameState, InGameState
from src.PacMan.renderer.strategies.imgs_loading_strategies import (
                                            BackgroundLoaderStrategy,
                                            BoardLoaderStrategy,
                                            ImageLoaderStrategy,
                                            LivesLoaderStrategy,
                                            MenuLoaderStrategy,
                                            GhostsLoaderStrategy,
                                            PacManLoaderStrategy)
from src.PacMan.renderer.strategies.text_loading_strategies import (
                                            TextLoaderStrategy,
                                            HubTextLoaderStrategy)
from src.PacMan.renderer.drawer_engine import BoardDrawerEngine


logger = logging.getLogger(__name__)


class RendererAssembler:
    def __init__(self, config: ValidBoardConfig) -> None:
        self._config = config
        self.cwd = Path(__file__).resolve().parent
        self._imgstrategies: dict[str, ImageLoaderStrategy] = {
            "background": BackgroundLoaderStrategy(),
            "board": BoardLoaderStrategy(),
            "lives": LivesLoaderStrategy(),
            "menus": MenuLoaderStrategy(),
            "ghosts": GhostsLoaderStrategy(),
            "pacman": PacManLoaderStrategy()
        }
        self._textstrategies: dict[str, TextLoaderStrategy] = {
            'hub': HubTextLoaderStrategy()
        }

    def init_glm(
            self,
            databasemng: DatabaseManager,
            cheat: bool = False,
            state: type[IGameState] = InGameState) -> GameLogicManager:
        try:
            return GameLogicManager(databasemng=databasemng,
                                    friendly_ghosts=cheat,
                                    start_state=state)
        except Exception:
            logger.error("FATAL: maze couldnot be made with following params: "
                         f"perfect True, seed 42, config: {self._config}")
            raise SystemExit(1)

    def init_drawer(self) -> BoardDrawerEngine:
        return BoardDrawerEngine(self._config)

    def init_engine(self) -> PyGMiniLibXEmulator:
        return PyGMiniLibXEmulator(self._config.size,
                                   self._config.size + 2 * int(
                                       self._config.size /
                                       self._config.hub_panels_prop
                                   ))

    def img_loader_dispatcher(
            self,
            folder: str,
            event: ConfiguratorT | None = None
    ) -> ImgsAsset:
        if 'live' in folder:
            return self._imgstrategies['lives'].load(folder, self)
        if 'background' in folder:
            return self._imgstrategies['background'].load(folder, self)
        if 'board' in folder:
            return self._imgstrategies['board'].load(folder, self, event)
        if 'menus' in folder:
            return self._imgstrategies['menus'].load(folder, self, event)
        if 'ghosts' in folder:
            return self._imgstrategies['ghosts'].load(folder, self, event)
        if 'pacman' in folder:
            return self._imgstrategies['pacman'].load(folder, self, event)

    def text_loader_dispatcher(
            self,
            folder: str,
            msg: str
            ) -> ImgsAsset:
        if 'hub' in folder:
            return self._textstrategies['hub'].upload_text(
                folder,
                msg,
                self
            )

