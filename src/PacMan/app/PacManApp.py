import logging
from src.PacMan.validation_contracts.valid_game_config import (
    ValidAppEntriesConfig,
    ValidBoardConfig)
from src.PacMan.validation_contracts.parser import DataProcessor
from src.PacMan.renderer.renderer_factory import RendererFactory

logger = logging.getLogger(__name__)


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
            print(maze.__dict__)
            pygmlx = renderer.init_engine()
            img = pygmlx.pygmlx_new_image(pygmlx.width,
                                          pygmlx.height)
            pixels, _, _ = img.pygget_data_addr()
            pixels[50:150, 50:150] = [255, 0, 0, 255]
            pygmlx.pygmlx_put_image_to_window(img, 0, 0)

        except Exception as err:
            logger.exception(err)
            raise SystemExit()
