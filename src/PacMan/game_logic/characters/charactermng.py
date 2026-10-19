from src.PacMan.game_logic.characters.ghosts import GhostManager
from src.PacMan.game_logic.characters.pacman import Pacman


class CharacterManager:
    def __init__(self):
        self.ghost_mng: GhostManager = GhostManager()
        self.pacman: Pacman = Pacman()

    def update(self) -> None:
        self.ghost_mng.update()
        self.pacman.update()
