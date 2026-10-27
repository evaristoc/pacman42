from src.PacMan.game_logic.ingame.maze.maze import Maze
from src.PacMan.game_logic.ingame.maze.tile import PelletState
from src.PacMan.game_logic.ingame.characters.ghosts.ghosts import GhostManager
from src.PacMan.game_logic.player import Player
from src.PacMan.game_logic.ingame.characters.pacman import Pacman
from src.PacMan.game_logic.score_mng import ScoreManager


class CollisionManager:
    def __init__(self, maze: Maze,
                 pacman: Pacman, 
                 ghostmng: GhostManager, 
                 player: Player, 
                 scoremng: ScoreManager) -> None:
        self.maze = maze:
        self.pacman = pacman:
        self.ghostmng = ghostmng:
        self.player = player
        self.scoremng = scoremng

    def update(self) -> None:
        pass

    def check_pacman_pellet_collisions(self):
        if self.pacman.position.pellet_state == PelletState.NORMALPELLET:
            self.scoremng.normal_pellet_eaten()
            self.pacman.position.collide_with_pacman()
        elif self.pacman.position.pellet_state == PelletState.POWERPELLET:
            self.scoremng.super_pellet_eaten()
            self.ghostmng.big_pellet_activated()
            self.pacman.position.collide_with_pacman()

    def check_pacman_ghost_collisions(self):
        
