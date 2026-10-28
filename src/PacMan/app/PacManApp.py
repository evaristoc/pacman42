import logging
from typing import Any
from src.PacMan.validation_contracts.valid_game_config import (
    ValidAppEntriesConfig,
    ValidBoardConfig)
from src.PacMan.validation_contracts.parser import DataProcessor
from src.PacMan.renderer.observer import Observer
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
        self.board: dict[str, PyGMLXImageEmulator] | None = None
        self.ghosts_imgs: dict[str, PyMLXPNGEmulator] | None = None
        self.pacman_imgs: dict[str, PyMLXPNGEmulator] | None = None
        self.menus_imgs: dict[str, PyGMLXTextEmulator] | None = None
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
                                                2 * bottom)
            self.glm = assembler.init_glm()
            self.maze = self.glm.maze
            self.board_img = assembler.init_board(size)
            rsized = self.drawer.resized
            self.ghosts_imgs = assembler.upload_imgs("ghosts",
                                                     rsized,
                                                     rsized)
            self.pacman_imgs = assembler.upload_imgs("pacman",
                                                     rsized,
                                                     rsized)
            self.menus_imgs = {}
            self.menus_imgs["start"] = assembler.upload_imgs(
                                                    "menu/start",
                                                    100,
                                                    60)
            self.menus_imgs["hub_u"] = assembler.init_hub_text(
                size,
                bottom,
                "Score 100  Highest 20000  Remaining 50secs",
                0,
                0,
                "CONSOLA.TTF",
                24
            )
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
            int(self.drawer.margin / 2),
            int(self.drawer.margin / 2) + self.drawer.bottom_h
            )
        # for i, img in enumerate(self.menus_imgs["start"].keys()):
        #     self.pygmlx.pygmlx_put_image_to_window(
        #         self.menus_imgs["start"][img],
        #         int(self.drawer.margin / 2) + 150,
        #         int(self.drawer.margin / 2) + self.drawer.bottom_h + i * 100
        #         )   
        # upper hub
        self.pygmlx.pygmlx_put_image_to_window(
            self.menus_imgs["hub_u"],
            int(self.drawer.margin / 2),
            int(self.drawer.margin / 2)
        )
        # lower hub
        level = self.pygmlx.pygmlx_new_text_image(
                                        98,
                                        48,
                                        24,
                                        0xF6303F
                                    )
        level.pygput_from_text(
            0,
            0,
            "Level 1"
        )
        self.pygmlx.pygmlx_put_image_to_window(
            level,
            0,
            int(self.drawer.margin / 2) + self.drawer.bottom_h + self.drawer.corrected_size[0]
        )

        self.pygmlx.pygmlx_put_image_to_window(
            self.pacman_imgs["still"],
            int(self.drawer.margin / 2) + 350,
            int(self.drawer.margin / 2) + self.drawer.bottom_h + self.drawer.corrected_size[0]
        )
        self.pygmlx.pygmlx_put_image_to_window(
            self.pacman_imgs["still"],
            int(self.drawer.margin / 2) + 350 + 30,
            int(self.drawer.margin / 2) + self.drawer.bottom_h + self.drawer.corrected_size[0]
        )
        self.pygmlx.pygmlx_put_image_to_window(
            self.pacman_imgs["still"],
            int(self.drawer.margin / 2) + 350 + 60,
            int(self.drawer.margin / 2) + self.drawer.bottom_h + self.drawer.corrected_size[0]
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
        observer.register_assets("menus", self.menus_imgs)
        self.pygmlx.pygmlx_loop(observer)
