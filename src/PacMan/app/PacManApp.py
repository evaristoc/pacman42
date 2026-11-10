import logging
from types import MethodType
from src.PacMan.validation_contracts.valid_game_config import (
    ValidAppEntriesConfig,
    ValidBoardConfig)
from src.PacMan.validation_contracts.parser import DataProcessor
from src.PacMan.renderer.game_loop import GameLoop
from src.PacMan.renderer.renderer_engine import PyGMiniLibXEmulator
from src.PacMan.renderer.renderer_assembler import RendererAssembler
from src.PacMan.renderer.drawer_engine import BoardDrawerEngine
from src.PacMan.renderer.assets import (
                                ImgsAsset,
                                Assets,
                                AssetRegistry)
from src.PacMan.game_logic.gamemanager.gamelogicmng import GameLogicManager
from src.PacMan.database.db_mng import DatabaseManager, create_database_mng

logger = logging.getLogger(__name__)


class PacManApp:
    def __init__(self) -> None:
        self.assembler: RendererAssembler | None = None
        self.drawer: BoardDrawerEngine | None = None
        self.pygmlx: PyGMiniLibXEmulator | None = None
        self.dbm: DatabaseManager | None = None
        self.glm: GameLogicManager | None = None
        self.assetregistry: AssetRegistry | None = None

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
                                                menuwithexit_eh,
                                                # mainmenu_eh,
                                                # pausemenu_eh
                                                )
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
            self.dbm = create_database_mng()
            self.glm = self.assembler.init_glm(self.dbm,
                                               self.assembler._config.cheat,
                                               MainMenuState)
            # TODO update nb_cells config before drawer
            self.drawer = self.assembler.init_drawer()
            # NOTE I need to compute before loading, need those values
            self.drawer.compute(self.assembler._config)
            self.pygmlx = self.assembler.init_engine()
            # self.maze = self.glm.session.maze
            background: ImgsAsset = self.assembler.img_loader_dispatcher(
                                        "background",
                                        None)
            board: ImgsAsset = self.assembler.img_loader_dispatcher(
                                        "board",
                                        self.drawer)
            # rsized = self.drawer.resized
            ghosts: ImgsAsset = self.assembler.img_loader_dispatcher(
                                        "ghosts",
                                        GhostName)
            pacman: ImgsAsset = self.assembler.img_loader_dispatcher(
                                        "pacman",
                                        InGameEvents)
            pacman.event_handler = MethodType(pacman_eh, pacman)
            main_menu: ImgsAsset = self.assembler.img_loader_dispatcher(
                                        "menus/main",
                                        MainMenuEvents)
            main_menu.event_handler = MethodType(menuwithexit_eh, main_menu)
            pause_menu: ImgsAsset = self.assembler.img_loader_dispatcher(
                                        "menus/pause",
                                        PauseMenuEvents)
            pause_menu.event_handler = MethodType(menuwithexit_eh, pause_menu)
            register_menu: ImgsAsset = self.assembler.img_loader_dispatcher(
                                        "menus/register",
                                        HighScoreRegisterEvents)
            # three lives
            hub_bottom_img: ImgsAsset = self.assembler.img_loader_dispatcher(
                                    "menus/hub_bottom/live",
                                    None)
            hub_top: ImgsAsset = self.assembler.text_loader_dispatcher(
                                        "top_hub",
                                        "Score: {:>8}    Remaining {:>4}secs",
                                    )
            hub_botton_text: ImgsAsset = self.assembler.text_loader_dispatcher(
                                        "bottom_hub",
                                        "Level: {:>3}",
                                    )
            init_assets: Assets = Assets(
                state_name='init',
                img_assets={
                    background.asset_name: background
                }
            )
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
            main_assets: Assets = Assets(
                state_name=MainMenuState.__name__,
                img_assets={
                    main_menu.asset_name: main_menu
                }
            )
            pause_assets: Assets = Assets(
                state_name=PauseMenuState.__name__,
                img_assets={
                    pause_menu.asset_name: pause_menu
                }
            )
            register_assets: Assets = Assets(
                state_name=HighScoreRegisterState.__name__,
                img_assets={
                    register_menu.asset_name: register_menu
                }
            )
            self.assetregistry = AssetRegistry(
               init=init_assets,
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
        if (
            self.pygmlx is not None
            and self.glm is not None
            and self.drawer is not None
            and self.assembler is not None
            and self.assetregistry is not None
        ):
            gameloop = GameLoop(self.pygmlx,
                                self.glm,
                                self.drawer,
                                self.assembler,
                                self.assetregistry)
            self.pygmlx.pygmlx_loop(gameloop)
