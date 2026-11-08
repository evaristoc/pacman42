from src.PacMan.game_logic.ingame.maze.maze import Maze
from src.PacMan.game_logic.ingame.maze.tile import PelletState
from src.PacMan.game_logic.ingame.characters.ghosts.ghosts import GhostManager, GhostName
from src.PacMan.game_logic.ingame.characters.ghosts.ghostsm import GhostCollision
from src.PacMan.game_logic.player import Player
from src.PacMan.game_logic.ingame.characters.pacman import Pacman
from src.PacMan.game_logic.score_mng import ScoreManager
from src.PacMan.game_logic.ingame.time.time import TimeManager
from src.PacMan.game_logic.ingame.update_outcome import UpdateOutcome


class CollisionDetector:
    """Pure collision detection logic — no dependencies, no side effects."""

    @staticmethod
    def check_positions_collide(
        pos1: tuple[float, float],
        pos2: tuple[float, float]
    ) -> bool:
        """Detect if two entities collide based on position."""
        if ((abs(pos1[0] - pos2[0]) < 0.5) and pos1[1] == pos2[1]):
            return True
        if ((abs(pos1[1] - pos2[1]) < 0.5) and pos1[0] == pos2[0]):
            return True
        return False


class CollisionManager:
    def __init__(
        self,
        maze: Maze,
        pacman: Pacman,
        ghostmng: GhostManager,
        player: Player,
        timemng: TimeManager,
        scoremng: ScoreManager,
        friendly_ghosts: bool,
        detector: CollisionDetector = CollisionDetector()
    ) -> None:
        self.maze = maze
        self.pacman = pacman
        self.ghostmng = ghostmng
        self.player = player
        self.scoremng = scoremng
        self.timemng = timemng
        self.friendly_ghosts = friendly_ghosts
        self.detector = detector

    def update(self) -> UpdateOutcome:
        if not self.friendly_ghosts:
            ghost_outcome = self._handle_ghost_collisions()
            if ghost_outcome.value[0]:  # game is over
                return ghost_outcome
        return self._handle_pellet_collisions()

    def _handle_ghost_collisions(self) -> UpdateOutcome:
        """Detect ghosts, then handle each collision."""
        collisions = self._detect_ghost_collisions()
        return self._apply_ghost_collision_effects(collisions)

    def _detect_ghost_collisions(self) -> dict[GhostName, GhostCollision]:
        """Pure detection — no side effects."""
        pacman_pos = self.pacman.interpolated_position
        collisions = {}
        for ghost in self.ghostmng.ghosts.values():
            if self.detector.check_positions_collide(ghost.interpolated_position, pacman_pos):
                collisions[ghost.name] = ghost.collide_with_pacman_and_does_ghost_die()
        return collisions

    def _apply_ghost_collision_effects(self, collisions: dict[GhostName, GhostCollision]) -> UpdateOutcome:
        """Handle the consequences of detected collisions."""
        result = UpdateOutcome.GAME_STILL_GOING
        for collision in collisions.values():
            match collision:
                case GhostCollision.GHOSTDIES:
                    self.scoremng.ghost_eaten()
                case GhostCollision.NOTHING:
                    continue
                case GhostCollision.GHOSTWINS:
                    if self.player.decrement_lives():
                        self.pacman.pacman_dies()
                        self.timemng.restart_countdown()
                        self.ghostmng.reset()
                        return UpdateOutcome.GAME_STILL_GOING
                    else:
                        return UpdateOutcome.ALL_LIVES_LOST
        return result

    def _handle_pellet_collisions(self) -> UpdateOutcome:
        """Detect and handle pellet collisions."""
        pellet_state = self.pacman.new_position.pellet_state
        if pellet_state == PelletState.NORMALPELLET:
            return self._handle_normal_pellet()
        elif pellet_state == PelletState.POWERPELLET:
            return self._handle_power_pellet()
        return UpdateOutcome.GAME_STILL_GOING

    def _handle_normal_pellet(self) -> UpdateOutcome:
        """Handle normal pellet collision."""
        self.scoremng.normal_pellet_eaten()
        self.pacman.new_position.pellet_eaten_by_pacman()
        return self._check_pellet_count()

    def _handle_power_pellet(self) -> UpdateOutcome:
        """Handle power pellet collision."""
        self.scoremng.super_pellet_eaten()
        self.ghostmng.big_pellet_activated()
        self.pacman.new_position.pellet_eaten_by_pacman()
        return self._check_pellet_count()

    def _check_pellet_count(self) -> UpdateOutcome:
        """Check if all pellets are eaten."""
        if self.maze.decrement_pellets():
            return UpdateOutcome.GAME_STILL_GOING
        return UpdateOutcome.ALL_PELLETS_EATEN
