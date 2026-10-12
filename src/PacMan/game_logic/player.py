from dataclasses import dataclass


@dataclass
class Player:
    """Represents a player profile with name, score, and lives.

    This dataclass holds persistent player data that can be serialized
    for storage and restored between game sessions.
    """
    name: str
    score: int = 0
    lives: int = 3

    def to_dict(self) -> dict:
        """Serialize player data to a dictionary for storage.

        Returns:
            dict: A dictionary containing name, score, and lives.
        """
        return {"name": self.name, "score": self.score, "lives": self.lives}

    @classmethod
    def from_dict(cls, data: dict) -> "Player":
        """Deserialize player data from a dictionary.

        Args:
            data: A dictionary containing 'name', 'score', and 'lives' keys.

        Returns:
            Player: A new Player instance with the data from the dictionary.
        """
        return cls(**data)
