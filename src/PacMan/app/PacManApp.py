import logging
from pathlib import Path
from src.PacMan.validation_contracts.valid_game_config import (
    ValidAppEntriesConfig,
    ValidBoardConfig)
from src.PacMan.validation_contracts.parser import DataProcessor
from src.PacMan.renderer.renderer_factory import RendererFactory

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
            renderer = RendererFactory(config)
            maze = renderer.init_maze()
            pygmlx = renderer.init_engine()
            print(pygmlx.view_w, pygmlx.view_h)
            imgmlxbg = pygmlx.pygmlx_new_image(pygmlx.view_w,
                                               pygmlx.view_h)
            renderer.draw(imgmlxbg,
                          maze.grid,
                          None)
            pygmlx.pygmlx_put_image_to_window(
                imgmlxbg,
                3,
                3
                )
            imgmlx01 = pygmlx.pygmlx_new_image(500, 500)
            img01_path = cwd.parent / 'assets' / 'ghosts' / 'orange.png'
            imgmlx01.pygput_from_png(str(img01_path))
            print("Loaded image successfully: "
                  f"{imgmlx01.width}x{imgmlx01.height}")
            imgmlx01.pygll_resize(
                int(pygmlx.view_w / (2 * config.nb_cells)),
                int(pygmlx.view_h / (2 * config.nb_cells))
                )
            pygmlx.pygmlx_put_image_to_window(
                imgmlx01,
                int(pygmlx.view_w / config.nb_cells * .4) + int(pygmlx.view_w / config.nb_cells - .7) * 11,
                int(pygmlx.view_w / config.nb_cells * .4)
                )
            imgmlx02 = pygmlx.pygmlx_new_image(500, 500)
            img02_path = cwd.parent / 'assets' / 'ghosts' / 'blue.png'
            imgmlx02.pygput_from_png(str(img02_path))
            imgmlx02.pygll_resize(
                int(pygmlx.view_w / (2 * config.nb_cells)),
                int(pygmlx.view_h / (2 * config.nb_cells))
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
