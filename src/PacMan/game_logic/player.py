from dataclasses import dataclass
from src.PacMan.app_config.config import PLAYER_LIVES


@dataclass(frozen=True)
class PlayerSnapshot:
    score: int
    lives: int
    level: int


@dataclass
class Player:
    """Represents a player profile with name, score, and lives.

    This dataclass holds persistent player data that can be serialized
    for storage and restored between game sessions.
    """
    score: int = 0
    lives: int = PLAYER_LIVES
    level: int = 1

    def view(self) -> PlayerSnapshot:
        return PlayerSnapshot(score=self.score,
                              lives=self.lives,
                              level=self.level)

    def decrement_lives(self) -> int | None:
        if self.lives == 0:
            return None
        else:
            self.lives -= 1
        return 1

    def set_name(self, new_name: str) -> None:
        self.name = new_name
