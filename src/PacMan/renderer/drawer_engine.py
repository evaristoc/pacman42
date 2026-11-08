import logging
from typing import cast, Any
from src.PacMan.validation_contracts.valid_game_config import (
    ValidBoardConfig)
from src.PacMan.renderer.renderer_engine import PyGMLXImageEmulator
from src.PacMan.game_logic.ingame.maze.tile import Tile
from src.PacMan.game_logic.ingame.maze.maze import (
                                            Maze,
                                            MazeFactory,
                                            TileSnapshot) 
from src.PacMan.renderer.renderer_engine import PyGMiniLibXEmulator

logger = logging.getLogger(__name__)


class BoardDrawerEngine:
    DEFAULT_COLORS = {
        "background": 0xFF5500FF,
        "fourtytwo": 0xFFFFFFFF,
        "entrance": 0xFF00FF00,
        "exit": 0xFFFF00FF,
        # "walls": 0xFF00AAAA,
        # "path": 0xFF00FF00,
        # "walls": 0xFF00FF00,
        "walls": 0x0101F2,
    }

    BOTTOMPARTSCREEN = 5

    def __init__(self, config: ValidBoardConfig) -> None:
        self._config = config
        self.__perc_wall = .2
        self.__perc_padding = .2
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
        self.__corrected_size = self.__interior_cell_size *\
            config.nb_cells + self.__wall_thickness * (config.nb_cells + 1)
        self.__diff = self._config.size - self.__corrected_size
        self.__padding = 0
        self.__padding = int(
            self.__interior_cell_size * self.__perc_padding
        )
        self.__cell_center = (
            self.__interior_cell_size - 2 * self.__padding
        )
        # self._config = config
        # self.__perc_wall = .2
        # self.__perc_padding = .2
        # self.__total_cell_size = int(
        #     self._config.size / self._config.nb_cells)
        #     # + self.__perc_wall * int(
        #     #     self._config.size / self._config.nb_cells
        #     # ))
        # self.__wall_thickness = int(
        #     self.__total_cell_size * self.__perc_wall
        # )
        # self.__interior_cell_size = (
        #     self.__total_cell_size - 2 * self.__wall_thickness
        # )
        # self.__corrected_size = self.__interior_cell_size *\
        #     config.nb_cells + 2 * self.__wall_thickness * config.nb_cells
        # self.__diff = self._config.size - self.__corrected_size
        # self.__padding = 0
        # self.__padding = int(
        #     self.__interior_cell_size * self.__perc_padding
        # )
        # self.__cell_center = (
        #     self.__interior_cell_size - 2 * self.__padding
        # )
        # print("in drawer", self.__corrected_size, self._config)

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
    
    @property
    def tot_cell_size(self) -> tuple[int, str]:
        return (
            self.__total_cell_size,
            "after correcting for initial size / num cells"
            )

    @property
    def interior_cell_size(self) -> tuple[int, str]:
        return (
                self.__interior_cell_size,
                "calculated as total cell size - wall thickness"
                )

    @property
    def wall_thickness(self) -> tuple[int, float, str]:
        return (
            self.__wall_thickness,
            self.__perc_wall,
            f"% calculated against interior cell size "
            f"{self.__interior_cell_size} : {self.__perc_wall}"
            )

    @property
    def corrected_size(self) -> tuple[int, int, str]:
        return (
            self.__corrected_size,
            self.__diff,
            "corrected size and diff against given size"
            )

    @property
    def bottom_h(self) -> int:
        return int(self.corrected_size[0] / self.BOTTOMPARTSCREEN)

    @property
    def margin(self) -> int:
        return int(self.corrected_size[1] / 2 )

    @property
    def resized(self) -> int:
        return int(self.corrected_size[0] / (2 * self._config.nb_cells))

    def next_char_coord(self, v: int) -> int:
        img_size = self.resized
        tot_cell_size = self.tot_cell_size[0]
        # internal placing of the image on the cell
        refpos = int((tot_cell_size - img_size) / 2)
        unit_step = (self.interior_cell_size[0]
                     + self.wall_thickness[0])
        margin = self.margin
        return refpos + unit_step * v + margin

    def draw(
        self,
        target_img: PyGMLXImageEmulator,
        state: Any | list[list[Tile]],
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
                    self.draw_cell_interior(
                        target_img,
                        c,
                        0x000000
                    )

    def draw_cell_interior(
        self,
        target_img: PyGMLXImageEmulator,
        cell: Tile,
        # cell: tuple[int, int],
        color: int
    ) -> None:
        """Draw interior area of a cell using computed geometry."""
        x_cell = cell.cell_position_x
        y_cell = cell.cell_position_y
        inter = self.__interior_cell_size
        wall = self.__wall_thickness
        start_x = wall + x_cell * (inter + wall)
        start_y = wall + y_cell * (inter + wall)
        x_area = inter
        y_area = inter
        for dy in range(y_area):
            for dx in range(x_area):
                if start_x + dx < self.__corrected_size and start_y + dy < self.__corrected_size:
                    target_img.pygput_pixel(start_x + dx, start_y + dy, color)
        if cell.has_pellet():
            self.__draw_pellet(target_img, cell, color=0xffffff)

    def __draw_pellet(
            self,
            target_img: PyGMLXImageEmulator,
            cell: Tile,
            color: int
    ):
        x_cell = cell.cell_position_x
        y_cell = cell.cell_position_y
        total = self.__total_cell_size
        center_x = x_cell + int(total / 2)
        center_y = y_cell + int(total / 2)
        if cell.pellet_state.value == 1:
            radius = int(self.__cell_center + self.__cell_center * 0.2)
        if cell.pellet_state.value == 2:
            radius = int(self.__cell_center + self.__cell_center * 3)
            color = 0x0011AAFF
        wall = self.__wall_thickness
        start_x = x_cell * (total - wall)
        start_y = y_cell * (total - wall)
        for dx in range(total):
            for dy in range(total):
                if ((dx - center_x)**2 + (dy - center_y)**2) < radius:
                    target_img.pygput_pixel(start_x + dx, start_y + dy, color) 

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
        # start_x = x_cell * inter + (2 * wall - wall) * x_cell
        # start_y = y_cell * inter + (2 * wall - wall) * y_cell
        start_x = x_cell * (total - wall)
        start_y = y_cell * (total - wall)
        print(start_x)
        if cell.wall_north.value != 1:
            for dx in range(total):
                for dy in range(wall):
                    if start_x + dx < self.__corrected_size and start_y + dy < self.__corrected_size:
                        target_img.pygput_pixel(start_x + dx,
                                                start_y + dy,
                                                color)
        if cell.wall_west.value != 1:
            for dx in range(wall):
                for dy in range(total):
                    if start_x + dx < self.__corrected_size and start_y + dy < self.__corrected_size:
                        target_img.pygput_pixel(start_x + dx,
                                                start_y + dy,
                                                color)
        if cell.wall_east.value != 1:
            wall_x = start_x + inter + wall
            for dx in range(wall):
                for dy in range(total):
                    if wall_x + dx < self.__corrected_size and start_y + dy < self.__corrected_size:
                        target_img.pygput_pixel(wall_x + dx,
                                                start_y + dy,
                                                color)
        if cell.wall_south.value != 1:
            wall_y = start_y + inter + wall
            for dy in range(wall):
                for dx in range(total):
                    if start_x + dx < self.__corrected_size and wall_y + dy < self.__corrected_size:
                        target_img.pygput_pixel(start_x + dx,
                                                wall_y + dy,
                                                color)

