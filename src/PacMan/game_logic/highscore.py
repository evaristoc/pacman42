from dataclasses import dataclass
from src.PacMan.database.db_mng import Player


@dataclass(frozen=True)
class HSPlayerSnapshot:
    rank: int
    name: str
    score: int


@dataclass(frozen=True)
class HighScoreSnapshot:
    highscores: list[HSPlayerSnapshot]


def db_highsc_to_snapshot(highscores: list[Player]
                          ) -> HighScoreSnapshot | None:
    if not highscores:
        return None
    hs_players: list[HSPlayerSnapshot] = [HSPlayerSnapshot(rank=i,
                                                           name=player.name,
                                                           score=player.score)
                                          for i, player in enumerate(highscores,
                                                                     start=1)]
    return HighScoreSnapshot(highscores=hs_players)
