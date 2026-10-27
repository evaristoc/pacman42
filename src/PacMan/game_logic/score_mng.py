from src.PacMan.game_logic.player import Player
from enum import Enum, auto


class ScoreEvents(Enum):
    PACMAN_EATS_NORMAL_PELLET = auto()
    PACMAN_EATS_SUPER_PELLET = auto()
    PACMAN_EATS_GHOST = auto()
    PLAYER_PASSES_LEVEL = auto()


class ScoreManager:
    SCORE_PER_EVENT: dict = {ScoreEvents.PACMAN_EATS_NORMAL_PELLET: 50,
                             ScoreEvents.PACMAN_EATS_SUPER_PELLET: 100,
                             ScoreEvents.PACMAN_EATS_GHOST: 200,
                             ScoreEvents.PLAYER_PASSES_LEVEL: 300}

    def __init__(self, player: Player) -> None:
        self.player = player

    def normal_pellet_eaten(self) -> None:
        self.player.score += self.SCORE_PER_EVENT[ScoreEvents.PACMAN_EATS_NORMAL_PELLET]

    def super_pellet_eaten(self) -> None:
        self.player.score += self.SCORE_PER_EVENT[ScoreEvents.PACMAN_EATS_SUPER_PELLET]

    def ghost_eaten(self) -> None:
        self.player.score += self.SCORE_PER_EVENT[ScoreEvents.PACMAN_EATS_GHOST]

    def player_passes_level(self) -> None:
        self.player.score += self.SCORE_PER_EVENT[ScoreEvents.PLAYER_PASSES_LEVEL]
