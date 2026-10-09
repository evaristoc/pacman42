import logging
from mazegenerator import MazeGenerator
from src.PacMan.validation_contracts.valid_game_config import ValidBoardConfig
from src.PacMan.renderer.renderer_engine import PyGMiniLibXEmulator, PyGMLXImageEmulator

logger = logging.getLogger(__name__)


class RendererFactory:
    def __init__(self, config: ValidBoardConfig) -> None:
        self._config = config

    def health_check(self) -> bool:
        if not PyGMiniLibXEmulator and not MazeGenerator:
            return False

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
        return PyGMiniLibXEmulator(self.width * 100,
                                   self.height * 100)


