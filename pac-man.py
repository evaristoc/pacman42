import logging
import fire
from pathlib import Path
from rich.console import Console
#import PacMan
from src import PacMan

console = Console()
logger = logging.getLogger(__name__)


class Controller:
    def load_game(self,
                  config: str) -> None:
        if not PacMan:
            console.log("[bold red]FATAL: library was not found.[/bold red]")
            raise SystemExit()
        console.print(PacMan)
        pacman = PacMan.PacMan()
        project_root = Path(__file__).resolve().parent
        path_to_config = str((project_root / Path(config)).resolve())
        valconfig = pacman.get_config(path_to_config=path_to_config)
        if not valconfig:
            console.log("[bold red]FATAL: library was not found.[/bold red]")
            raise SystemExit()
        console.print(valconfig)
        pacman.init_board(config=valconfig.board)     


if __name__ == "__main__":
    # python pac-man.py load_game --config configs/configs.json
    try:
        fire.Fire(Controller)
    except Exception as err:
        logger.exception(err)
        console.print("FATAL: the following error ocurred:"
                      f"{type(err)} : {err}")
        raise SystemExit()
