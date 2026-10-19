import logging
from typing import cast
from src.PacMan.renderer.renderer_engine import PyGMLXImageEmulator
from src.PacMan.game_logic.maze.tile import Tile
from src.PacMan.game_logic.maze.maze import Maze, MazeFactory
from src.PacMan.validation_contracts.valid_game_config import ValidBoardConfig
from src.PacMan.renderer.renderer_engine import PyGMiniLibXEmulator

logger = logging.getLogger(__name__)


class RendererFactory:
    DEFAULT_COLORS = {
        "background": 0xFF5500FF,
        "fourtytwo": 0xFFFFFFFF,
        "entrance": 0xFF00FF00,
        "exit": 0xFFFF00FF,
        # "walls": 0xFF00AAAA,
        # "path": 0xFF00FF00,
        "walls": 0xFF00FF00,
    }

    def __init__(self, config: ValidBoardConfig) -> None:
        self._config = config
        self.__perc_wall = .2
        # self.__perc_padding = .2
        self.__total_cell_size = int(
            self._config.size / self._config.nb_cells
            + self.__perc_wall * int(
                self._config.size / self._config.nb_cells
            ))
        self.__wall_thickness = int(
            self.__total_cell_size * self.__perc_wall
        )
        self.__interior_cell_size = (
            self.__total_cell_size - 2 * self.__wall_thickness
        )
        # self.__padding = int(
        #     self.__interior_cell_size * self.__perc_padding
        # )
        # self.__cell_center = (
        #     self.__interior_cell_size - 2 * self.__padding
        # )

    def init_maze(self) -> Maze:
        try:
            return MazeFactory(self._config.nb_cells).make_map()
        except Exception:
            logger.error("FATAL: maze couldnot be made with following params: "
                         f"perfect True, seed 42, config: {self._config}")

    def init_engine(self) -> PyGMiniLibXEmulator:
        if self._config.size is not None:
            return PyGMiniLibXEmulator(self._config.size,
                                       self._config.size)
        else:
            logger.error("FATAL: height or width found to be None.")
            raise SystemExit()

    def draw(
        self,
        target_img: PyGMLXImageEmulator,
        state: list[list[Tile | tuple[Tile, str]]],
        els: dict[str, int] | None
    ) -> None:
        """Render maze cells, walls, and overlays onto target image."""
        elements = self.DEFAULT_COLORS if not els else els
        # if "background" in elements:
        #     self.__draw_all_background(
        #         target_img,
        #         # cast(list[list[Tile]], state),
        #         elements["background"]
        #     )
        for r in state:
            for c in r:
                if "walls" in elements:
                    self.__draw_cell_walls(
                        target_img,
                        cast(Tile, c),
                        elements["walls"]
                    )
                # if "fourtytwo" in elements and isinstance(c, FourtyTwoCell):
                #     self.__draw_cell_interior(
                #         target_img,
                #         cast(Cell, c),
                #         elements["fourtytwo"]
                #     )
                # if "entrance" in elements and isinstance(c, EntryCell):
                #     self.__draw_cell_interior(
                #         target_img,
                #         cast(Cell, c),
                #         elements["entrance"]
                #     )
                # if "exit" in elements and isinstance(c, ExitCell):
                #     self.__draw_cell_interior(
                #         target_img,
                #         cast(Cell, c),
                #         elements["exit"]
                #     )

    # def __get_total_size(
    #     self,
    #     num_cells_x: int,
    #     num_cells_y: int
    # ) -> tuple[int, int]:
    #     """Compute total pixel size from maze grid dimensions."""
    #     total_w = (
    #         num_cells_x * self.__total_cell_size
    #         - self.__wall_thickness * (num_cells_x - 1)
    #     )
    #     total_h = (
    #         num_cells_y * self.__total_cell_size
    #         - self.__wall_thickness * (num_cells_y - 1)
    #     )
    #     # total_w = self._config.size / self._config.nb_cells
    #     # total_h = total_w
    #     return total_w, total_h

    # def __draw_all_background(
    #     self,
    #     target_img: PyGMLXImageEmulator,
    #     # state: list[list[Tile]],
    #     color: int
    # ) -> None:
    #     """Fill entire maze render area with background color."""
    #     pix_tot_w, pix_tot_h = self.__get_total_size(
    #         # len(state[0]), len(state)
    #     )
    #     for y in range(pix_tot_h):
    #         for x in range(pix_tot_w):
    #             target_img.pygput_pixel(x, y, color)

    # def __draw_cell_interior(
    #     self,
    #     target_img: Image,
    #     cell: Cell,
    #     color: int
    # ) -> None:
    #     """Draw interior area of a cell using computed geometry."""
    #     x_cell = cell.cell_position_x
    #     y_cell = cell.cell_position_y
    #     inter = self.__interior_cell_size
    #     wall = self.__wall_thickness
    #     pad = self.__padding
    #     if isinstance(cell, FourtyTwoCell):
    #         start_x = wall + x_cell * (inter + wall) + pad * 2
    #         start_y = wall + y_cell * (inter + wall) + pad // 2
    #         x_area = self.__cell_center
    #         y_area = self.__cell_center
    #     elif isinstance(cell, (ExitCell, EntryCell)):
    #         start_x = wall + x_cell * (inter + wall) + pad
    #         start_y = wall + y_cell * (inter + wall) + pad
    #         x_area = self.__cell_center
    #         y_area = self.__cell_center
    #     else:
    #         start_x = wall + x_cell * (inter + wall)
    #         start_y = wall + y_cell * (inter + wall)
    #         x_area = inter
    #         y_area = inter
    #     for dy in range(y_area):
    #         for dx in range(x_area):
    #             target_img.put_pixel(start_x + dx, start_y + dy, color)

    def __draw_cell_walls(
        self,
        target_img: PyGMLXImageEmulator,
        cell: Tile,
        color: int
    ) -> None:
        """Draw visible walls of a cell based on wall flags."""
        x_cell = cell.cell_position_x
        y_cell = cell.cell_position_y
        # print("in draw cell walls", x_cell, y_cell)
        total = self.__total_cell_size
        wall = self.__wall_thickness
        inter = self.__interior_cell_size
        start_x = x_cell * (total - wall)
        start_y = y_cell * (total - wall)
        if cell.wall_north.value != 1:
            for dx in range(total):
                for dy in range(wall):
                    target_img.pygput_pixel(start_x + dx, start_y + dy, color)
        if cell.wall_west.value != 1:
            for dx in range(wall):
                for dy in range(total):
                    target_img.pygput_pixel(start_x + dx, start_y + dy, color)
        if cell.wall_east.value != 1:
            wall_x = start_x + inter + wall
            for dx in range(wall):
                for dy in range(total):
                    target_img.pygput_pixel(wall_x + dx, start_y + dy, color)
        if cell.wall_south.value != 1:
            wall_y = start_y + inter + wall
            for dy in range(wall):
                for dx in range(total):
                    target_img.pygput_pixel(start_x + dx, wall_y + dy, color)
