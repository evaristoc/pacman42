import logging
from mazegenerator import MazeGenerator
from src.PacMan.validation_contracts.valid_game_config import ValidBoardConfig
from src.PacMan.renderer.renderer_engine import PyGMiniLibXEmulator

logger = logging.getLogger(__name__)


class RendererFactory:
    def __init__(self, config: ValidBoardConfig) -> None:
        self._config = config

    def init_maze(self) -> MazeGenerator:
        try:
            return MazeGenerator(size=(self._config.width,
                                       self._config.height),
                                 perfect=True,
                                 seed=42)
        except Exception:
            logger.error("FATAL: maze couldnot be made with following params: "
                         f"perfect True, seed 42, config: {self._config}")

    def init_engine(self) -> PyGMiniLibXEmulator:
        if self._config.height is not None and self._config.width is not None:
            return PyGMiniLibXEmulator(self._config.width * 100,
                                       self._config.height * 100)
        else:
            logger.error("FATAL: height or width found to be None.")
            raise SystemExit()


