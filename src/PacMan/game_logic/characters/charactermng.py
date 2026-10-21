from src.PacMan.game_logic.characters.ghosts import GhostManager
from src.PacMan.game_logic.characters.pacman import Pacman
from src.PacMan.game_logic.maze.maze import Maze


class CharacterManager:
    def __init__(self, maze: Maze) -> None:
        self.pacman: Pacman = Pacman(maze)
        self.ghost_mng: GhostManager = GhostManager(maze)

    def update(self, delta_ticks: int) -> None:
        # self.pacman.update()
        self.ghost_mng.update(delta_ticks, self.pacman.get_position())
