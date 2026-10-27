from src.PacMan.game_logic.ingame.maze.maze import Maze
from src.PacMan.game_logic.ingame.maze.tile import PelletState
from src.PacMan.game_logic.ingame.characters.ghosts.ghosts import GhostManager
from src.PacMan.game_logic.player import Player
from src.PacMan.game_logic.ingame.characters.pacman import Pacman
from src.PacMan.game_logic.score_mng import ScoreManager
from src.PacMan.game_logic.ingame.time.time import TimeManager


class CollisionManager:
    def __init__(self, maze: Maze,
                 pacman: Pacman,
                 ghostmng: GhostManager,
                 player: Player,
                 timemng: TimeManager,
                 scoremng: ScoreManager) -> None:
        self.maze = maze
        self.pacman = pacman
        self.ghostmng = ghostmng
        self.player = player
        self.scoremng = scoremng
        self.timemng = timemng

    def update(self) -> tuple[bool, bool | None]:
        game_over_and_level_won = self.check_pacman_ghost_collisions()
        if game_over_and_level_won[0]:
            return game_over_and_level_won
        return self.check_pacman_pellet_collisions()

    def check_pacman_pellet_collisions(self) -> tuple[bool, bool | None]:
        game_over = False
        level_won = None
        if self.pacman.position.pellet_state == PelletState.NORMALPELLET:
            self.scoremng.normal_pellet_eaten()
            self.pacman.position.pellet_eaten_by_pacman()
            print(
                f"Pacman ate normal pellet at position {self.pacman.position.get_position_from_tile()}")
            if self.maze.decrement_pellets():
                return (game_over, level_won)
            else:
                game_over = True
                level_won = True
                return (game_over, level_won)

        elif self.pacman.position.pellet_state == PelletState.POWERPELLET:
            self.scoremng.super_pellet_eaten()
            self.ghostmng.big_pellet_activated()
            self.pacman.position.pellet_eaten_by_pacman()
            print(
                f"Pacman ate super pellet at position {self.pacman.position.get_position_from_tile()}")
            if self.maze.decrement_pellets():
                return (game_over, level_won)
            else:
                game_over = True
                level_won = True
                return (game_over, level_won)
        return (game_over, level_won)

    def check_pacman_ghost_collisions(self) -> tuple[bool, bool | None]:
        game_over = False
        level_won = None
        pacman_position = self.pacman.position
        for ghost in self.ghostmng.ghosts.values():
            if ghost.position == pacman_position and ghost.state:
                ghost_dies = ghost.collide_with_pacman_and_does_ghost_die()
                if ghost_dies:
                    self.scoremng.ghost_eaten()
                    print(
                        f"Pacman ate {ghost.name.name} ghost at position {pacman_position}")
                    return (game_over, level_won)
                else:
                    if self.player.decrement_lives():
                        self.pacman.pacman_dies()
                        self.timemng.restart_countdown()
                        print(
                            f"Ghost {ghost.name.name} ate pacman at {pacman_position}")
                        return (game_over, level_won)
                    else:
                        game_over = True
                        level_won = False
                        return (game_over, level_won)
        return (game_over, level_won)
