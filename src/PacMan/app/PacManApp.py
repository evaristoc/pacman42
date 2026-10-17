import logging
from pathlib import Path
from src.PacMan.validation_contracts.valid_game_config import (
    ValidAppEntriesConfig,
    ValidBoardConfig)
from src.PacMan.validation_contracts.parser import DataProcessor
from src.PacMan.renderer.renderer_assembler import RendererAssembler

logger = logging.getLogger(__name__)
cwd = Path(__file__).resolve().parent


class PacManApp:
    def __str__(self) -> str:
        return "I am PacMan!"

    def get_config(self, path_to_config: str) -> ValidAppEntriesConfig:
        # path_to_config: str = str(Path.cwd / 'configs' / 'configs.json')
        raw_data = DataProcessor.load_dataset(path_to_config)
        return DataProcessor.resolve_and_validate(**raw_data)

    def init_board(self, config: ValidBoardConfig) -> None:
        try:
            renderer = RendererAssembler(config)
            maze = renderer.init_maze()
            pygmlx = renderer.init_engine()
            drawer = renderer.init_drawer()
            print(pygmlx.view_w, pygmlx.view_h)
            print(drawer.tot_cell_size[0])
            print(drawer.interior_cell_size[0])
            print(drawer.wall_thickness[0])
            print(drawer.corrected_size[0], drawer.corrected_size[1])  
            imgmlxbg = pygmlx.pygmlx_new_image(drawer.corrected_size[0],
                                               drawer.corrected_size[0])
         
            drawer.draw(imgmlxbg,
                        maze.grid,
                        None)
            # cell_size = int(pygmlx.view_w / config.nb_cells)
            pygmlx.pygmlx_put_image_to_window(
                imgmlxbg,
                int(drawer.corrected_size[1] / 2),
                int(drawer.corrected_size[1] / 2)
                )
            imgmlx01 = pygmlx.pygmlx_new_image(500, 500)
            img01_path = cwd.parent / 'assets' / 'ghosts' / 'orange.png'
            imgmlx01.pygput_from_png(str(img01_path))
            print("Loaded image successfully: "
                  f"{imgmlx01.width}x{imgmlx01.height}")
            img_resize = int(pygmlx.view_w / (2 * config.nb_cells))
            imgmlx01.pygll_resize(
                img_resize,
                img_resize
                )
            # print(cell_size)
            # print(img_resize)
            # print((cell_size - img_resize) / 2)
            # print((cell_size - 2 * cell_size * .2 - img_resize) / 2)
            # print(drawer.tot_cell_size)
            # padding = (cell_size - 2 * cell_size * .2 - img_resize) / 2
            pygmlx.pygmlx_put_image_to_window(
                imgmlx01,
                # int(pygmlx.view_w / config.nb_cells * .4) + int(pygmlx.view_w / config.nb_cells - .7) * 3,
                # int(pygmlx.view_w / config.nb_cells * .4)
                int((drawer.tot_cell_size[0] - img_resize) / 2) + (drawer.interior_cell_size[0] + drawer.wall_thickness[0]) * 6 + int(drawer.corrected_size[1] / 2),
                int((drawer.tot_cell_size[0] - img_resize) / 2) + (drawer.interior_cell_size[0] + drawer.wall_thickness[0]) * 7 + int(drawer.corrected_size[1] / 2)
                # int(cell_size * .2 + padding) + cell_size * 0,
                # int(cell_size * .2 + padding) + cell_size * 9,
                )
            imgmlx02 = pygmlx.pygmlx_new_image(500, 500)
            img02_path = cwd.parent / 'assets' / 'ghosts' / 'blue.png'
            imgmlx02.pygput_from_png(str(img02_path))
            imgmlx02.pygll_resize(
                img_resize,
                img_resize
                )
            print("Loaded image successfully: "
                  f"{imgmlx02.width}x{imgmlx02.height}")
            pygmlx.pygmlx_put_image_to_window(
                imgmlx02,
                int(pygmlx.view_w / 3),
                int(pygmlx.view_w / 3)
                )
            pygmlx.pygmlx_loop()
            # img = pygmlx.pygmlx_new_image(pygmlx.width,
            #                               pygmlx.height)
            # pixels, _, _ = img.pygget_data_addr()
            # pixels[50:150, 50:150] = [255, 0, 0, 255]
            # pygmlx.pygmlx_put_image_to_window(img, 0, 0)
        except Exception as err:
            logger.exception(err)
            raise SystemExit(1)
