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
                                TextMetadata,
                                ImgsAsset,
                                Assets
                                )
# from src.PacMan.game_logic.maze.maze import Maze, MazeFactory
from src.PacMan.database.db_mng import DatabaseManager
from src.PacMan.game_logic.gamemanager.gamelogicmng import GameLogicManager
from src.PacMan.game_logic.ingame.characters.ghosts.ghosts import GhostName
from src.PacMan.renderer.renderer_engine import (PyGMiniLibXEmulator,
                                                 PyGMLXImageEmulator,
                                                 PyMLXPNGEmulator,
                                                 PyGMLXTextEmulator)
from src.PacMan.game_logic.gamemanager.game_sm import IGameState, InGameState

logger = logging.getLogger(__name__)


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

    def init_glm(self, databasemng: DatabaseManager, state: IGameState = InGameState) -> GameLogicManager:
        try:
            return GameLogicManager(databasemng, state)
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
            sources={
                'board': source
            }
        )

    def upload_imgs(
            self,
            folder: str,
            metadata: ImgMetadata,
            event: GhostName | IEventEnums | None = None
            ) -> ImgsAsset:
        _assets = self.cwd.parent / 'assets' / folder
        if event:
            print(folder, vars(event))
            _names = getattr(event, '_member_names_')
            if event.__name__ == 'GhostName':
                _names = _names + ['DEAD', 'POWERUP']
            if folder == 'pacman':
                _names.remove('PAUSE')
                _temp_sources: list[Source] = []
                _files = [f'{n}-{str(v)}' for v in range(1, 4, 1) for n in _names]
        else:
            # lives
            _names = [folder.split('/')[-1].upper() for i in range(3)]
        imgassets: ImgsAsset = ImgsAsset(asset_name=folder.split('/')[-1])
        try:
            for stem in _names:
                if folder != 'pacman':
                    print(folder, stem)
                    path = _assets / Path(stem + '.png')
                    if not path.is_file():
                        logger.exception(f"FATAL: we could not load image : {path}")
                        raise SystemExit(1)
                    with Image.open(path) as img:
                        org_w, org_h = img.size
                    # print(fname, org_w)
                    img = PyMLXPNGEmulator(
                                org_w,
                                org_h
                            )
                    img.pygput_from_png(
                                str(path)
                            )
                    rsize_w = int(org_w * metadata.resize_w_prop)
                    rsize_h = int(org_h * metadata.resize_h_prop)
                    img.pygll_resize(
                                rsize_w,
                                rsize_h
                            )
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
                else:
                    for f in _files:
                        if stem in f:
                            path = _assets / stem / Path(f + '.png')
                            if not path.is_file():
                                logger.exception(f"FATAL: we could not load image : {path}")
                                raise SystemExit(1)
                            with Image.open(path) as img:
                                org_w, org_h = img.size
                            # print(fname, org_w)
                            img = PyMLXPNGEmulator(
                                        org_w,
                                        org_h
                                    )
                            img.pygput_from_png(
                                        str(path)
                                    )
                            rsize_w = int(org_w * metadata.resize_w_prop)
                            rsize_h = int(org_h * metadata.resize_h_prop) 
                            img.pygll_resize(
                                        rsize_w,
                                        rsize_h
                                    )
                            source = Source(
                                event_name=f,
                                path=path,
                                img=img,
                                metadata=metadata
                            )
                            _temp_sources.append(source)
                            # imgassets.sources.update(
                            #     {
                            #         f: source
                            #     }
                if folder == 'pacman':
                    for e in _names:
                        q = []
                        for s in _temp_sources:
                            if e in s.event_name:
                                q.append(s)
                        q = sorted(
                            q,
                            key=lambda iats: int(iats.event_name.split('-')[-1])
                        )
                        imgassets.sources[e] = deque(q)
                        #         imgassets.sources.update(
                        #             {
                        #              asset_name: e,
                        #              sources: s
                        #              })
                        # imgassets.sources = deque(sorted(
                        #     imgassets.sources,
                        #     key=lambda iats: int(iats.asset_name.split('-')[-1])
                        # ))
                    # if folder == 'pacman':
                    #     source = Source(
                    #         event_name=stem,
                    #         path=path,
                    #         img=img,
                    #         metadata=metadata
                    #     )
                    #     _temp_sources.append(source) 
            return imgassets
        except Exception as err:
            logger.exception(f"FATAL: we could not load images : {err}")
            raise SystemExit(1)

    def upload_hub_text(
            self,
            asset_name: str,
            w: int,
            h: int,
            msg: str,
            start_x: int,
            start_y: int,
            metadata: TextMetadata
            ) -> ImgsAsset:
        imgasset: ImgsAsset = ImgsAsset(asset_name=asset_name)
        metadata.text = msg
        source = Source(
            img=PyGMLXTextEmulator(
                            w,
                            h,
                            metadata.font_path,
                            int(w * metadata.font_size_prop),
                            metadata.color
                            )
        )
        source.img.pygput_from_text(
                            start_x,
                            start_y,
                            metadata.text)
        imgasset.sources.update(
            {
                asset_name: source
            }
        )
        return imgasset
