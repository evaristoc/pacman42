import os
import logging
from pathlib import Path
from src.PacMan.renderer.drawer_engine import DrawerEngine
from src.PacMan.game_logic.map.map import Map, MapFactory
from src.PacMan.validation_contracts.valid_game_config import ValidBoardConfig
from src.PacMan.renderer.renderer_engine import (PyGMiniLibXEmulator,
                                                 PyGMLXImageEmulator,
                                                 PyMLXPNGEmulator)

logger = logging.getLogger(__name__)


class RendererAssembler:
    def __init__(self, config: ValidBoardConfig) -> None:
        self._config = config
        self.cwd = Path(__file__).resolve().parent

    def init_maze(self) -> Map:
        try:
            return MapFactory(self._config.nb_cells).make_map()
        except Exception:
            logger.error("FATAL: maze couldnot be made with following params: "
                         f"perfect True, seed 42, config: {self._config}")

    def init_engine(self, v_width: int, v_height: int) -> PyGMiniLibXEmulator:
        if self._config.size is not None:
            return PyGMiniLibXEmulator(v_width,
                                       v_height)
        else:
            logger.error("FATAL: height or width found to be None.")
            raise SystemExit()

    def init_drawer(self) -> DrawerEngine:
        return DrawerEngine(self._config)

    def init_ghosts(
            self,
            width: int,
            height: int) -> dict[str, PyMLXPNGEmulator]:
        # ghosts
        ghost_assets = self.cwd.parent / 'assets' / 'ghosts'
        ghost_dict = {}
        for r, d, files in os.walk(ghost_assets):
            fname = Path(files).name
            if fname not in ghost_dict:
                ghost_dict[fname] = PyMLXPNGEmulator()


    def init_board(self) -> PyGMLXImageEmulator:
        # maze

    def init_pacman(self) -> dict[str, PyGMLXImageEmulator]:
        # pacman
