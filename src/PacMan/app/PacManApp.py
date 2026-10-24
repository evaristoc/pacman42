import logging
from typing import Any
from src.PacMan.validation_contracts.valid_game_config import (
    ValidAppEntriesConfig,
    ValidBoardConfig)
from src.PacMan.validation_contracts.parser import DataProcessor
from src.PacMan.app.observer import Observer
from src.PacMan.renderer.renderer_engine import (
                                PyGMiniLibXEmulator,
                                PyGMLXImageEmulator,
                                PyMLXPNGEmulator,
                                PyGMLXTextEmulator)
from src.PacMan.renderer.renderer_assembler import RendererAssembler
from src.PacMan.renderer.drawer_engine import DrawerEngine
from src.PacMan.game_logic.gamemanager.gamelogicmng import GameLogicManager

logger = logging.getLogger(__name__)


class PacManApp:
    def __init__(self) -> None:
        self.assembler: RendererAssembler | None = None
        self.drawer: DrawerEngine | None = None
        self.pygmlx: PyGMiniLibXEmulator | None = None
        self.glm: GameLogicManager | None = None
        self.board: dict[PyGMLXImageEmulator] | None = None
        self.ghosts_imgs: dict[PyMLXPNGEmulator] | None = None
        self.pacman_imgs: dict[PyMLXPNGEmulator] | None = None
        self.assets: dict[str, Any] | None = None

    def __str__(self) -> str:
        return "I am PacMan!"

    def get_config(self, path_to_config: str) -> ValidAppEntriesConfig:
        # path_to_config: str = str(Path.cwd / 'configs' / 'configs.json')
        raw_data = DataProcessor.load_dataset(path_to_config)
        return DataProcessor.resolve_and_validate(**raw_data)

    def load_game(self, config: ValidBoardConfig) -> None:
        """
        gets config and keep the state of initial values to
        assemble the whole board relative to those values
        """
        try:
            # assembler is a short live object only for assembling
            assembler = RendererAssembler(config)
            # drawer will control all relevant metrics
            # it will also paint the canvas
            self.drawer = assembler.init_drawer()
            size = self.drawer.corrected_size[0]
            bottom = self.drawer.bottom_h
            self.pygmlx = assembler.init_engine(config.size,
                                                bottom)
            self.glm = assembler.init_glm()
            self.maze = self.glm.maze
            self.board_img = assembler.init_board(size)
            rsized = self.drawer.resized
            self.ghosts_imgs = assembler.upload_imgs("ghosts",
                                                     rsized)
            self.pacman_imgs = assembler.upload_imgs("pacman",
                                                     rsized)
            # self.assets = self.board_img | self.ghosts_imgs | self.pacman_imgs
        except Exception as err:
            logger.exception(err)
            raise SystemExit(1)

    def run(self) -> None:
        """
        mount the different parts and start the game
        """
        # if self.drawer is None or self.pygmlx is None or self.maze is None or self.board_img is None or self.ghosts_imgs is None or self.pacman_imgs is None:
        #     logger.exception("FATAL: no assembler was defined.")
        #     raise SystemExit(1)
        self.drawer.draw(self.board_img,
                         self.maze.grid,
                         None)
        # print(
        #     self.drawer.corrected_size[0],
        #     self.drawer.corrected_size[1],
        #     self.drawer.margin)
        # board_margin = int(self.drawer.corrected_size[1] / 2)
        self.pygmlx.pygmlx_put_image_to_window(
            self.board_img,
            self.drawer.margin / 2,
            self.drawer.margin / 2
            )
        # print(self.ghosts_imgs)
        # for i, g in enumerate(self.ghosts_imgs):
        #     self.pygmlx.pygmlx_put_image_to_window(
        #         self.ghosts_imgs[g],
        #         self.drawer.next_char_coord(i),
        #         self.drawer.next_char_coord(0)
        #     )
        # for i, p in enumerate(self.pacman_imgs):
        #     self.pygmlx.pygmlx_put_image_to_window(
        #         self.pacman_imgs[p],
        #         self.drawer.next_char_coord(i),
        #         self.drawer.next_char_coord(1)
        #     )
        # imgmlxtext: PyGMLXTextEmulator = self.pygmlx.pygmlx_new_text_image(
        #     self.drawer.corrected_size[0],
        #     self.drawer.bottom_h,
        #     40)
        # imgmlxtext.pygput_from_text(0, 0, "I am Pacman.")
        # self.pygmlx.pygmlx_put_image_to_window(
        #     imgmlxtext,
        #     14,
        #     self.drawer.corrected_size[0] + 7,
        # )
        observer = Observer(self.pygmlx, self.glm, self.drawer)
        observer.register_assets("ghosts", self.ghosts_imgs)
        observer.register_assets("pacman", self.pacman_imgs)
        observer.register_assets("board", self.board_img)
        self.pygmlx.pygmlx_loop(observer)
