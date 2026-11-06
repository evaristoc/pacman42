import logging
from types import MethodType
from src.PacMan.validation_contracts.valid_game_config import (
    ValidAppEntriesConfig,
    ValidBoardConfig)
from src.PacMan.validation_contracts.parser import DataProcessor
from src.PacMan.renderer.observer import Observer
from src.PacMan.renderer.renderer_engine import PyGMiniLibXEmulator
from src.PacMan.renderer.renderer_assembler import RendererAssembler
from src.PacMan.renderer.drawer_engine import DrawerEngine
from src.PacMan.renderer.assets import (
                                ImgsAsset,
                                ImgMetadata,
                                TextMetadata,
                                Assets,
                                AssetRegistry)
from src.PacMan.game_logic.gamemanager.gamelogicmng import GameLogicManager


logger = logging.getLogger(__name__)

class PacManApp:
    def __init__(self) -> None:
        self.assembler: RendererAssembler | None = None
        self.drawer: DrawerEngine | None = None
        self.pygmlx: PyGMiniLibXEmulator | None = None
        self.glm: GameLogicManager | None = None
        self.assetregistry: AssetRegistry | None = None
        # self.board: dict[str, PyGMLXImageEmulator] | None = None
        # self.characters_imgs: dict[
        #     str,
        #     dict[str, PyMLXPNGEmulator | list[PyMLXPNGEmulator]]] | None = {
        #                                             "InGameEvents": {
        #                                                 "pacman": {},
        #                                                 "ghosts": {}
        #                                             }}
        # self.menus_imgs: dict[str, dict[str, PyGMLXTextEmulator]] | None = {}
        # self.assets: dict[str, Any] | None = None

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
        from src.PacMan.validation_contracts.event_enums import (
                                            InGameEvents,
                                            MainMenuEvents,
                                            PauseMenuEvents,
                                            HighScoreRegisterEvents)
        from src.PacMan.renderer.event_handlers import (
                                                pacman_eh,
                                                mainmenu_eh,
                                                pausemenu_eh)
        from src.PacMan.game_logic.gamemanager.game_sm import (
                                                InGameState,
                                                MainMenuState,
                                                PauseMenuState,
                                                HighScoreRegisterState)
        from src.PacMan.game_logic.ingame.characters.ghosts.ghosts import (
                                                GhostName)
        try:
            # assembler is a short live object only for assembling
            self.assembler = RendererAssembler(config)
            # drawer will control all relevant metrics
            # it will also paint the canvas
            self.drawer = self.assembler.init_drawer()
            size = self.drawer.corrected_size[0]
            bottom = self.drawer.bottom_h
            self.pygmlx = self.assembler.init_engine(config.size,
                                                2 * bottom)
            self.glm = self.assembler.init_glm(InGameState)
            self.maze = self.glm.session.maze
            board: ImgsAsset = self.assembler.load_board(size, size)
            # rsized = self.drawer.resized
            char_meta: ImgMetadata = ImgMetadata(
                resize_w_prop=1/(2 * self.assembler._config.nb_cells),
                resize_h_prop=1/(2 * self.assembler._config.nb_cells)
            )
            ghosts: ImgsAsset = self.assembler.upload_imgs(
                                        "ghosts",
                                        char_meta,
                                        GhostName)
            pacman: ImgsAsset = self.assembler.upload_imgs(
                                        "pacman",
                                        char_meta,
                                        InGameEvents)
            menu_meta: ImgMetadata = ImgMetadata(
                resize_w_prop=1/5,
                resize_h_prop=1/8,
                gap_y_prop=1/50
            )
            main_menu: ImgsAsset = self.assembler.upload_imgs(
                                        "menus/main",
                                        menu_meta,
                                        MainMenuEvents)
            pause_menu: ImgsAsset = self.assembler.upload_imgs(
                                        "menus/pause",
                                        menu_meta,
                                        PauseMenuEvents)
            register_menu: ImgsAsset = self.assembler.upload_imgs(
                                        "menus/register",
                                        menu_meta,
                                        HighScoreRegisterEvents)
            # three lives
            hub_bottom_img: ImgsAsset = self.assembler.upload_imgs(
                                    "menus/hub_bottom/live",
                                    char_meta)
            hub_meta: TextMetadata = TextMetadata(
                resize_w_prop=1/5,
                resize_h_prop=1/10
            )
            hub_top: ImgsAsset = self.assembler.upload_hub_text(
                                        "top_text",
                                        size,
                                        bottom,
                                        "Score: {:>8}    Remaining {:>4}secs",
                                        0,
                                        0,
                                        hub_meta
                                    )
            hub_botton_text: ImgsAsset = self.assembler.upload_hub_text(
                                        "bottom_text",
                                        size,
                                        bottom,
                                        "Level: {:>3}",
                                        0,
                                        0,
                                        hub_meta
                                    )
            # self.assets = self.board_img | self.ghosts_imgs | self.pacman_imgs
            ingame_assets: Assets = Assets(
                state_name=InGameState.__name__,
                img_assets={
                    ghosts.asset_name: ghosts,
                    pacman.asset_name: pacman,
                    board.asset_name: board,
                    hub_top.asset_name: hub_top,
                    hub_bottom_img.asset_name: hub_bottom_img,
                    hub_botton_text.asset_name: hub_botton_text
                },
            )
            ingame_assets.event_handler = MethodType(pacman_eh, ingame_assets)
            main_assets: Assets = Assets(
                state_name=MainMenuState.__name__,
                img_assets={
                    main_menu.asset_name: main_menu
                }
            )
            main_assets.event_handler = MethodType(mainmenu_eh, main_assets)
            pause_assets: Assets = Assets(
                state_name=PauseMenuState.__name__,
                img_assets={
                    pause_menu.asset_name: pause_menu
                }
            )
            pause_assets.event_handler = MethodType(pausemenu_eh, main_assets)
            register_assets: Assets = Assets(
                state_name=HighScoreRegisterState.__name__,
                img_assets={
                    register_menu.asset_name: register_menu
                }
            )
            self.assetregistry = AssetRegistry(
               ingamestate=ingame_assets,
               mainmenustate=main_assets,
               pausemenustate=pause_assets,
               highscoreregisterstate=register_assets 
            ) 

        except Exception as err:
            logger.exception(err)
            raise SystemExit(1)

    def run(self) -> None:
        """
        mount the different parts and start the game
        """
        print(self.assetregistry)
        Observer(self.pygmlx, self.glm, self.drawer, self.assembler._config.size)
        self.pygmlx.pygmlx_loop(observer)
        # # if self.drawer is None or self.pygmlx is None or self.maze is None or self.board_img is None or self.ghosts_imgs is None or self.pacman_imgs is None:
        # #     logger.exception("FATAL: no assembler was defined.")
        # #     raise SystemExit(1)
        # self.drawer.draw(self.board_img,
        #                  self.maze.grid,
        #                  None)
        # # print(
        # #     self.drawer.corrected_size[0],
        # #     self.drawer.corrected_size[1],
        # #     self.drawer.margin)
        # # board_margin = int(self.drawer.corrected_size[1] / 2)
        # self.pygmlx.pygmlx_put_image_to_window(
        #     self.board_img,
        #     int(self.drawer.margin / 2),
        #     int(self.drawer.margin / 2) + self.drawer.bottom_h
        #     )
        # # for i, img in enumerate(self.menus_imgs["start"].keys()):
        # #     self.pygmlx.pygmlx_put_image_to_window(
        # #         self.menus_imgs["start"][img],
        # #         int(self.drawer.margin / 2) + 150,
        # #         int(self.drawer.margin / 2) + self.drawer.bottom_h + i * 100
        # #         )   
        # # upper hub
        # self.pygmlx.pygmlx_put_image_to_window(
        #     self.menus_imgs["hub_u"],
        #     int(self.drawer.margin / 2),
        #     int(self.drawer.margin / 2)
        # )
        # # lower hub
        # level = self.pygmlx.pygmlx_new_text_image(
        #                                 int(self.assembler._config.size / 5),
        #                                 int(self.assembler._config.size / 10),
        #                                 int(self.assembler._config.size / 20),
        #                                 0xF6303F
        #                             )
        # level.pygput_from_text(
        #     0,
        #     0,
        #     "Level 1"
        # )
        # self.pygmlx.pygmlx_put_image_to_window(
        #     level,
        #     0,
        #     int(self.drawer.margin / 2) + self.drawer.bottom_h + self.drawer.corrected_size[0]
        # )
        # # print(self.characters_imgs)
        # self.pygmlx.pygmlx_put_image_to_window(
        #     self.characters_imgs["InGameEvents"]["pacman"]["START"],
        #     int(self.drawer.margin / 2) + int(0.7 * self.assembler._config.size),
        #     int(self.drawer.margin / 2) + self.drawer.bottom_h + self.drawer.corrected_size[0]
        # )
        # self.pygmlx.pygmlx_put_image_to_window(
        #     self.characters_imgs["InGameEvents"]["pacman"]["START"],
        #     int(self.drawer.margin / 2) + int(0.7 * self.assembler._config.size) + int(0.06 * self.assembler._config.size),
        #     int(self.drawer.margin / 2) + self.drawer.bottom_h + self.drawer.corrected_size[0]
        # )
        # self.pygmlx.pygmlx_put_image_to_window(
        #     self.characters_imgs["InGameEvents"]["pacman"]["START"],
        #     int(self.drawer.margin / 2) + int(0.7 * self.assembler._config.size) + int(0.12 * self.assembler._config.size),
        #     int(self.drawer.margin / 2) + self.drawer.bottom_h + self.drawer.corrected_size[0]
        # )
        # observer = Observer(self.pygmlx, self.glm, self.drawer, self.assembler._config.size)
        # observer.register_assets("board", self.board_img)
        # observer.register_assets("InGameState", self.characters_imgs["InGameEvents"])
        # observer.register_assets("MainMenuState", self.menus_imgs["MainMenuEvents"])
        # observer.register_assets("HighScoreMenuState", self.menus_imgs["HighScoreRegisterEvents"])
        # observer.register_assets("PauseMenuState", self.menus_imgs["PauseMenuEvents"])
        # observer.register_assets("GameOverState", self.menus_imgs["GameOver"])
        # self.pygmlx.pygmlx_loop(observer)
