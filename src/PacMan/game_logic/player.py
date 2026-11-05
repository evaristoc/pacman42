from dataclasses import dataclass


@dataclass(frozen=True)
class PlayerSnapshot:
    name: str
    score: int
    lives: int
    level: int


@dataclass
class Player:
    """Represents a player profile with name, score, and lives.

    This dataclass holds persistent player data that can be serialized
    for storage and restored between game sessions.
    """
    name: str
    score: int = 0
    lives: int = 0
    level: int = 1

    def view(self) -> PlayerSnapshot:
        return PlayerSnapshot(name=self.name,
                              score=self.score,
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
