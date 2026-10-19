import logging
from src.PacMan.validation_contracts.valid_game_config import (
    ValidAppEntriesConfig,
    ValidBoardConfig)
from src.PacMan.validation_contracts.parser import DataProcessor
from src.PacMan.renderer.drawer_engine import PyGMX
from src.PacMan.renderer.renderer_assembler import RendererAssembler
from src.PacMan.renderer.drawer_engine import DrawerEngine

logger = logging.getLogger(__name__)


class PacManApp:
    def __init__(self) -> None:
        self.assembler: RendererAssembler | None = None
        self.drawer: DrawerEngine | None = None
        self.pygmlx: PyGMiniLibXEmulator | None = None
        self.maze: Map | None = None
        self.board: dict[] | None = None
        self.ghosts_imgs: dict[] | None = None
        self.pacman_imgs: dict[] | None = None

    def __str__(self) -> str:
        return "I am PacMan!"

    def get_config(self, path_to_config: str) -> ValidAppEntriesConfig:
        # path_to_config: str = str(Path.cwd / 'configs' / 'configs.json')
        raw_data = DataProcessor.load_dataset(path_to_config)
        return DataProcessor.resolve_and_validate(**raw_data)

    @classmethod
    def init_game(cls, config: ValidBoardConfig) -> None:
        """
        gets config and keep the state of initial values to
        assemble the whole board relative to those values
        """
        try:
            # assembler is a short live object only for assembling
            assembler = RendererAssembler(config)
            # drawer will control all relevant metrics
            # it will also paint the canvas
            cls.drawer = assembler.init_drawer()
            size = cls.drawer.corrected_size[0]
            bottom = cls.drawer.bottom_h
            cls.pygmlx = assembler.init_engine(size,
                                               bottom)
            cls.maze = assembler.init_maze()
            cls.board_img = assembler.init_board(size)
            rsized = cls.drawer.resized
            cls.ghosts_imgs = assembler.register_imgs(rsized,
                                                      "ghosts")
            cls.pacman_imgs = assembler.register_imgs(rsized,
                                                      "pacman")

        except Exception as err:
            logger.exception(err)
            raise SystemExit(1)

    def run(self) -> None:
        """
        mount the different parts and start the game
        """
        if self.drawer is None or self.pygmlx is None or self.maze is None or self.board_img is None or self.ghosts_imgs is None or self.pacman_imgs is None:
            logger.exception("FATAL: no assembler was defined.")
            raise SystemExit(1)
        self.drawer.draw(self.board_img["board"],
                         self.maze.grid,
                         None)
        # cell_size = int(pygmlx.view_w / config.nb_cells)
        self.pygmlx.pygmlx_put_image_to_window(
            self.board_img["board"],
            int(self.drawer.corrected_size[1] / 2),  # margins
            int(self.rawer.corrected_size[1] / 2)
            )
        
        for i, g in enumerate(self.ghosts_imgs):
            self.pygmlx.pygmlx_put_image_to_window(
                self.ghosts_imgs[g],
                int((drawer.tot_cell_size[0] - img_refpos) / 2)
                + (drawer.interior_cell_size[0]
                   + drawer.wall_thickness[0]) * i
                + int(drawer.corrected_size[1] / 2),
                int((drawer.tot_cell_size[0] - img_refpos) / 2)
                + (drawer.interior_cell_size[0]
                   + drawer.wall_thickness[0]) * 0
                + int(drawer.corrected_size[1] / 2)
            )
        for i, g in enumerate(pacman_imgs):
            self.pygmlx.pygmlx_put_image_to_window(
                self.ghosts_imgs[g],
                int((drawer.tot_cell_size[0] - img_refpos) / 2)
                + (drawer.interior_cell_size[0]
                   + drawer.wall_thickness[0]) * i
                + int(drawer.corrected_size[1] / 2),
                int((drawer.tot_cell_size[0] - img_refpos) / 2)
                + (drawer.interior_cell_size[0]
                   + drawer.wall_thickness[0]) * 0
                + int(drawer.corrected_size[1] / 2)
            )
        imgmlxtext = pygmlx.pygmlx_new_text_image(
            drawer.corrected_size[0],
            0)
        imgmlxtext.pygput_from_text(0, 0, "I am Pacman.")
        pygmlx.pygmlx_put_image_to_window(
            imgmlxtext,
            14,
            drawer.corrected_size[0] + 7,
        )
        pygmlx.pygmlx_loop()

    def _next_char_coord(self, v: int) -> int:
        img_size = int(
            self.assembler.ref_w / (2 * self.assembler._config.nb_cells)
            )
        img_refpos = int((self.drawer.tot_cell_size[0] - img_refpos) / 2)
        return
