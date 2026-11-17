import logging
from pathlib import Path
from src.PacMan.validation_contracts.valid_game_config import ValidBoardConfig
from src.PacMan.renderer.assets import ImgsAsset
from src.PacMan.database.db_mng import DatabaseManager
from src.PacMan.game_logic.gamemanager.gamelogicmng import GameLogicManager
from src.PacMan.renderer.renderer_engine import PyGMiniLibXEmulator
from src.PacMan.game_logic.gamemanager.game_sm import IGameState, InGameState
from src.PacMan.renderer.asset_factories.imgs_loading_factory import (
                                            ConfiguratorT,
                                            BackgroundLoader,
                                            BoardLoader,
                                            ImageLoader,
                                            ReturnLoader,
                                            LivesLoader,
                                            MenuLoader,
                                            GameOverLoader,
                                            GhostsLoader,
                                            PacManLoader)
from src.PacMan.renderer.asset_factories.text_loading_factory import (
                                            TextLoader,
                                            HubTextLoader,
                                            InstructionsTextLoader)
from src.PacMan.renderer.drawer_engine import BoardDrawerEngine


logger = logging.getLogger(__name__)


class RendererAssembler:
    def __init__(self, config: ValidBoardConfig) -> None:
        self._config = config
        self.drawer: BoardDrawerEngine = BoardDrawerEngine()
        self.cwd = Path(__file__).resolve().parent
        self._imgasset_map: dict[str, ImageLoader] = {
            "background": BackgroundLoader(),
            "board": BoardLoader(),
            "lives": LivesLoader(),
            "instructions": ReturnLoader(),
            "menus": MenuLoader(),
            "ghosts": GhostsLoader(),
            "pacman": PacManLoader(),
            "gameoverlost": GameOverLoader(),
            "gameoverwon": GameOverLoader()
        }
        self._textasset_map: dict[str, TextLoader] = {
            'hub': HubTextLoader(),
            'instructions': InstructionsTextLoader()
        }

    def init_glm(
            self,
            databasemng: DatabaseManager,
            cheat: bool = False,
            level_skip: bool = False,
            state: type[IGameState] = InGameState) -> GameLogicManager:
        try:
            return GameLogicManager(databasemng=databasemng,
                                    friendly_ghosts=cheat,
                                    level_skip=level_skip,
                                    start_state=state)
        except Exception:
            logger.error("FATAL: maze couldnot be made with following params: "
                         f"perfect True, seed 42, config: {self._config}")
            raise SystemExit(1)

    def init_drawer(self) -> None:
        self.drawer.compute(self._config)

    def init_engine(self) -> PyGMiniLibXEmulator:
        if self._config and self._config.size and self._config.hub_panels_prop:
            return PyGMiniLibXEmulator(self._config.size,
                                       self._config.size + 2 * int(
                                        self._config.size /
                                        self._config.hub_panels_prop
                                        ))
        else:
            logger.error("FATAL: we could not get the size to build "
                         "the emulator (init_engine)")
            raise SystemExit(1)

    def img_loader_factdispatcher(
            self,
            folder: str,
            event: ConfiguratorT | None = None
    ) -> ImgsAsset:
        if 'live' in folder:
            return self._imgasset_map['lives'].load(folder, self)
        if 'gameoverlost' in folder:
            return self._imgasset_map['gameoverlost'].load(folder, self, event)
        if 'gameoverwon' in folder:
            return self._imgasset_map['gameoverwon'].load(folder, self, event)
        if 'instructions' in folder:
            return self._imgasset_map['instructions'].load(folder, self, event)
        # above the ones that ALSO might contain 'menus' word in folder
        if 'menus' in folder:
            return self._imgasset_map['menus'].load(folder, self, event)
        if 'background' in folder:
            return self._imgasset_map['background'].load(folder, self)
        if 'board' in folder:
            return self._imgasset_map['board'].load(folder, self)
        if 'ghosts' in folder:
            return self._imgasset_map['ghosts'].load(folder, self, event)
        if 'pacman' in folder:
            return self._imgasset_map['pacman'].load(folder, self, event)
        return ImgsAsset()

    def text_loader_factdispatcher(
            self,
            folder: str,
            msg: str
            ) -> ImgsAsset:
        if 'hub' in folder:
            return self._textasset_map['hub'].upload_text(
                folder,
                msg,
                self
            )
        if 'instructions' in folder:
            return self._textasset_map['instructions'].upload_text(
                folder,
                msg,
                self
            )
        return ImgsAsset()
