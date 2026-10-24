import logging
from collections import deque
from pathlib import Path
from PIL import Image
from src.PacMan.validation_contracts.valid_game_config import ValidBoardConfig
from src.PacMan.renderer.drawer_engine import DrawerEngine
# from src.PacMan.game_logic.maze.maze import Maze, MazeFactory
from src.PacMan.game_logic.gamemanager.gamelogicmng import GameLogicManager
from src.PacMan.renderer.renderer_engine import (PyGMiniLibXEmulator,
                                                 PyGMLXImageEmulator,
                                                 PyMLXPNGEmulator)

logger = logging.getLogger(__name__)

# REFWITHNOTSETVALUE = -1
# BOTTOMPARTSCREEN = 5


class RendererAssembler:
    def __init__(self, config: ValidBoardConfig) -> None:
        self._config = config
        self.cwd = Path(__file__).resolve().parent

    # @property
    # def ref_w(self) -> int:
    #     return self._reference_w

    # @ref_w.setter
    # def ref_w(self, val: int) -> None:
    #     self._reference_w = val

    def init_glm(self) -> GameLogicManager:
        try:
            return GameLogicManager(self._config.nb_cells)
        except Exception:
            logger.error("FATAL: maze couldnot be made with following params: "
                         f"perfect True, seed 42, config: {self._config}")

    def init_drawer(self) -> DrawerEngine:
        return DrawerEngine(self._config)

    def init_engine(self, w: int, bottom_h: int) -> PyGMiniLibXEmulator:
        return PyGMiniLibXEmulator(w,
                                   w + bottom_h)        
        # if self.ref_w == REFWITHNOTSETVALUE:
        #     logger.exception("FATAL: we could not set ref size.")
        #     raise SystemExit(1)
        # return PyGMiniLibXEmulator(w,
        #                            w + w / BOTTOMPARTSCREEN)

    def init_board(self, w: int) -> dict[str, PyGMLXImageEmulator]:
        # maze
        return {
            "board":
                PyMLXPNGEmulator(
                    w,
                    w
                )}

    def register_imgs(
            self,
            rsize: int,
            character: str) -> dict[str, PyMLXPNGEmulator]:
        # assume ref size cannot be negative, but it could...
        # if self.ref_w == REFWITHNOTSETVALUE:
        #     logger.exception("FATAL: we could not set ref size.")
        #     raise SystemExit(1)
        _assets = self.cwd.parent / 'assets' / character
        _dict: dict[str, PyMLXPNGEmulator] = {}
        try:
            # this will sort the paths (they are Path types now)
            sorted_files = sorted(_assets.rglob('*'))
            for file in sorted_files:
                if not file.is_file():
                    continue
                with Image.open(_assets / file) as img:
                    org_w, org_h = img.size
                fname = Path(file).stem
                print(fname, org_w)
                emu = PyMLXPNGEmulator(
                            org_w,
                            org_h
                        )
                emu.pygput_from_png(
                            str(_assets / file)
                        )
                emu.pygll_resize(
                            rsize,
                            rsize
                        )
                if "pacman" in file.parts:
                    if "pacman" not in _dict:
                        _dict["pacman"]["moves"] = deque([])
                        _dict["pacman"]["still"] = None
                    if fname == "1":
                        _dict["pacman"]["still"] = emu
                    _dict["pacman"]["moves"].append(emu)
                else:
                    if fname not in _dict:
                        _dict[fname] = emu
            return _dict
        except Exception as err:
            logger.exception(f"FATAL: we could not load images : {err}")
            raise SystemExit(1)
