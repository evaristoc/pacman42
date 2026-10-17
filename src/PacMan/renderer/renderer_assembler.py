import logging
from src.PacMan.renderer.drawer_engine import DrawerEngine
from src.PacMan.game_logic.map.map import Map, MapFactory
from src.PacMan.validation_contracts.valid_game_config import ValidBoardConfig
from src.PacMan.renderer.renderer_engine import PyGMiniLibXEmulator

logger = logging.getLogger(__name__)


class RendererAssembler:
    def __init__(self, config: ValidBoardConfig) -> None:
        self._config = config

    def init_maze(self) -> Map:
        try:
            return MapFactory(self._config.nb_cells).make_map()
        except Exception:
            logger.error("FATAL: maze couldnot be made with following params: "
                         f"perfect True, seed 42, config: {self._config}")

    def init_engine(self) -> PyGMiniLibXEmulator:
        if self._config.size is not None:
            return PyGMiniLibXEmulator(self._config.size,
                                       self._config.size)
        else:
            logger.error("FATAL: height or width found to be None.")
            raise SystemExit()

    def init_drawer(self) -> DrawerEngine:
        return DrawerEngine(self._config)
