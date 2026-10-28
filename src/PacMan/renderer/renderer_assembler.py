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
                                                 PyMLXPNGEmulator,
                                                 PyGMLXTextEmulator)

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

    def init_engine(
            self,
            w: int,
            bottom_h: int
            ) -> PyGMiniLibXEmulator:
        return PyGMiniLibXEmulator(w,
                                   w + bottom_h)        
        # if self.ref_w == REFWITHNOTSETVALUE:
        #     logger.exception("FATAL: we could not set ref size.")
        #     raise SystemExit(1)
        # return PyGMiniLibXEmulator(w,
        #                            w + w / BOTTOMPARTSCREEN)

    def init_board(self, w: int) -> PyGMLXImageEmulator:
        # maze
        return PyMLXPNGEmulator(
                    w,
                    w
                )

    def upload_imgs(
            self,
            folder: str,
            rsize_w: int | None = None,
            rsize_h: int | None = None) -> dict[str, PyMLXPNGEmulator]:
        # assume ref size cannot be negative, but it could...
        # if self.ref_w == REFWITHNOTSETVALUE:
        #     logger.exception("FATAL: we could not set ref size.")
        #     raise SystemExit(1)
        _assets = self.cwd.parent / 'assets' / folder
        _dict: dict[str, PyMLXPNGEmulator] = {}
        try:
            # this will sort the paths (they are Path types now)
            sorted_files = sorted(_assets.rglob('*'))
            print(sorted_files)
            for file in sorted_files:
                if not file.is_file():
                    continue
                with Image.open(_assets / file) as img:
                    org_w, org_h = img.size
                fname = Path(file).stem
                # print(fname, org_w)
                emu = PyMLXPNGEmulator(
                            org_w,
                            org_h
                        )
                emu.pygput_from_png(
                            str(_assets / file)
                        )
                if rsize_w and rsize_h:
                    emu.pygll_resize(
                                rsize_w,
                                rsize_h
                            )
                print(file.parts)
                if "pacman" == file.parts[-2]:
                    if "moves" not in _dict:
                        _dict = {
                            "moves": deque([]),
                            "still": None
                        }
                    if fname == "1":
                        _dict["still"] = emu
                    _dict["moves"].append(emu)
                else:
                    if fname not in _dict:
                        _dict[fname] = emu
            print(_dict)
            return _dict
        except Exception as err:
            logger.exception(f"FATAL: we could not load images : {err}")
            raise SystemExit(1)

    def init_hubs(
            self,
            w: int,
            h: int,
            msg: str,
            x: int,
            y: int,
            font_path: str = "CONSOLA.TTF",
            font_size: int = 14,
            color: int = 0xF6303F,
            # color: int = 0xffffff
            ) -> PyGMLXTextEmulator:
        imgmlxtext = PyGMLXTextEmulator(
            w,
            h,
            font_path,
            font_size,
            color)
        imgmlxtext.pygput_from_text(
            x,
            y,
            msg)
        return imgmlxtext
