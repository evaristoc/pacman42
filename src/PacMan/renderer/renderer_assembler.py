import logging
from collections import deque
from pathlib import Path
from PIL import Image
from typing import Any
from src.PacMan.validation_contracts.event_enums import (
                                            InGameEvents,
                                            IEventEnums)
from src.PacMan.validation_contracts.valid_game_config import ValidBoardConfig
from src.PacMan.renderer.drawer_engine import DrawerEngine
from src.PacMan.renderer.assets import (
                                Source,
                                ImgMetadata,
                                ImgsAsset,
                                Assets
                                )
# from src.PacMan.game_logic.maze.maze import Maze, MazeFactory
from src.PacMan.game_logic.gamemanager.gamelogicmng import GameLogicManager
from src.PacMan.game_logic.ingame.characters.ghosts.ghosts import GhostName
from src.PacMan.renderer.renderer_engine import (PyGMiniLibXEmulator,
                                                 PyGMLXImageEmulator,
                                                 PyMLXPNGEmulator,
                                                 PyGMLXTextEmulator)
from src.PacMan.game_logic.gamemanager.game_sm import IGameState, InGameState

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

    def init_glm(self, state: IGameState = InGameState) -> GameLogicManager:
        try:
            return GameLogicManager(state)
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

    def load_board(self,
                   w: int,
                   h: int) -> ImgsAsset:
        # maze
        source = Source(
            img=PyGMLXImageEmulator(
                    w,
                    h
                )
        )
        return ImgsAsset(
            asset_name='board',
            sources=source
        )

    # def upload_ghosts_imgs(
    #         self,
    #         folder: str,
    #         rsize_w: int | None = None,
    #         rsize_h: int | None = None,
    #         metadata: ImgMetadata | None = None
    #         # event: IEventEnums | None = None
    #         ) -> ImgsAsset:
    #     _assets = self.cwd.parent / 'assets' / folder

    #     imgassets: ImgsAsset = ImgsAsset(asset_name=folder)
    #     try:
    #         for stem in ghosts_names:
    #             path = _assets / Path(stem + '.png')
    #             if not path.is_file():
    #                 logger.exception(f"FATAL: we could not load image : {path}")
    #                 raise SystemExit(1)
    #             with Image.open(path) as img:
    #                 org_w, org_h = img.size
    #             # print(fname, org_w)
    #             if metadata:
    #                 img = PyMLXPNGEmulator(
    #                             org_w,
    #                             org_h
    #                         )
    #                 img.pygput_from_png(
    #                             str(path)
    #                         )
    #                 if metadata:
    #                     rsize_w = int(org_w * metadata.resize_w_prop)
    #                     rsize_h = int(org_h * metadata.resize_h_prop) 
    #                     img.pygll_resize(
    #                                 rsize_w,
    #                                 rsize_h
    #                             )
    #                     source = Source(
    #                         path=path,
    #                         img=img,
    #                         metadata=metadata
    #                     )
    #                     imgassets.sources.update(
    #                         {
    #                             stem: source
    #                         }
    #                     )
    #         return imgassets
    #     except Exception as err:
    #         logger.exception(f"FATAL: we could not load images : {err}")
    #         raise SystemExit(1)

    # def upload_menu_imgs(
    #         self,
    #         folder: str,
    #         rsize_w: int | None = None,
    #         rsize_h: int | None = None,
    #         metadata: ImgMetadata | None = None,
    #         event: IEventEnums | None = None
    #         ) -> ImgsAsset:
    #     _assets = self.cwd.parent / 'assets' / folder
    #     _names = IEventEnums.__members__.keys()
    #     imgassets: ImgsAsset = ImgsAsset(asset_name=folder)
    #     try:
    #         for stem in _names:
    #             path = _assets / Path(stem + '.png')
    #             if not path.is_file():
    #                 logger.exception(f"FATAL: we could not load image : {path}")
    #                 raise SystemExit(1)
    #             with Image.open(path) as img:
    #                 org_w, org_h = img.size
    #             # print(fname, org_w)
    #             if metadata:
    #                 img = PyMLXPNGEmulator(
    #                             org_w,
    #                             org_h
    #                         )
    #                 img.pygput_from_png(
    #                             str(path)
    #                         )
    #                 if metadata:
    #                     rsize_w = int(org_w * metadata.resize_w_prop)
    #                     rsize_h = int(org_h * metadata.resize_h_prop) 
    #                     img.pygll_resize(
    #                                 rsize_w,
    #                                 rsize_h
    #                             )
    #                     source = Source(
    #                         path=path,
    #                         img=img,
    #                         metadata=metadata
    #                     )
    #                     imgassets.sources.update(
    #                         {
    #                             stem: source
    #                         }
    #                     )
    #         return imgassets
    #     except Exception as err:
    #         logger.exception(f"FATAL: we could not load images : {err}")
    #         raise SystemExit(1)

    def upload_imgs(
            self,
            folder: str,
            rsize_w: int | None = None,
            rsize_h: int | None = None,
            metadata: ImgMetadata | None = None,
            event: GhostName | IEventEnums | None = None
            ) -> ImgsAsset:
        _assets = self.cwd.parent / 'assets' / folder
        if event.__name__ == 'GhostName':
            _names = GhostName.__members__.keys()
            _names = _names + ['DEAD', 'POWERUP']
        else:
            _names = event.__members__.keys()
            if folder == 'pacman':
                _names.remove('PAUSE')
                _pacmanE = _names[:]
                _temp_sources: list[Source] = []
                _names = [f'{n}-v' for v in range(1, 4, 1) for n in _names]
        imgassets: ImgsAsset = ImgsAsset(asset_name=folder.split('/')[-1])
        try:
            for stem in _names:
                path = _assets / Path(stem + '.png')
                if not path.is_file():
                    logger.exception(f"FATAL: we could not load image : {path}")
                    raise SystemExit(1)
                with Image.open(path) as img:
                    org_w, org_h = img.size
                # print(fname, org_w)
                if metadata:
                    img = PyMLXPNGEmulator(
                                org_w,
                                org_h
                            )
                    img.pygput_from_png(
                                str(path)
                            )
                    if metadata:
                        rsize_w = int(org_w * metadata.resize_w_prop)
                        rsize_h = int(org_h * metadata.resize_h_prop) 
                        img.pygll_resize(
                                    rsize_w,
                                    rsize_h
                                )
                        if folder == 'pacman':
                            source = Source(
                                event_name=stem,
                                path=path,
                                img=img,
                                metadata=metadata
                            )
                            _temp_sources.append(source) 
                        else:
                            source = Source(
                                path=path,
                                img=img,
                                metadata=metadata
                            )
                            imgassets.sources.update(
                                {
                                    stem: source
                                }
                            )
            if folder == 'pacman':
                for e in _pacmanE:
                    for s in _temp_sources:
                        if e in s.event_name:
                            imgassets.sources.append(s)
                    imgassets.sources = deque(sorted(
                        imgassets.sources,
                        key=lambda iats: int(iats.asset_name.split('-')[-1])
                    ))
            return imgassets
        except Exception as err:
            logger.exception(f"FATAL: we could not load images : {err}")
            raise SystemExit(1)

    def upload_pacman_imgs(
            self,
            folder: str,
            rsize_w: int | None = None,
            rsize_h: int | None = None) -> dict[str, PyMLXPNGEmulator]:
        # assume ref size cannot be negative, but it could...
        # if self.ref_w == REFWITHNOTSETVALUE:
        #     logger.exception("FATAL: we could not set ref size.")
        #     raise SystemExit(1)
        # print(dict(vars(event))['_member_names_'])
        _dict: dict[str, PyMLXPNGEmulator] = {}
        for e in ['PACMAN_NORTH', 'PACMAN_EAST', 'PACMAN_SOUTH', 'PACMAN_WEST']:
            _assets = self.cwd.parent / 'assets' / folder / e
            # print(_assets)
            try:
                # this will sort the paths (they are Path types now)
                sorted_files = sorted(_assets.rglob('*'))
                # print(sorted_files)
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
                    # print(file.parts)
                    if "pacman" == file.parts[-3]:
                        if e not in _dict:
                            _dict[e] = deque([])
                        if "START" not in _dict and fname == 'EAST-1':
                            _dict["START"] = emu
                        _dict[e].append(emu)
                    else:
                        if fname not in _dict:
                            _dict[fname] = emu
            except Exception as err:
                logger.exception(f"FATAL: we could not load images : {err}")
                raise SystemExit(1)
        # print(_dict)
        return _dict

    def init_hub_text(
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
