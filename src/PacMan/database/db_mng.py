from peewee import SqliteDatabase, Database, Model, CharField, IntegerField, DateTimeField, DoesNotExist
from src.PacMan.database.db_path import get_db_path
from datetime import datetime
from typing import List


class Player(Model):
    name = CharField(max_length=100, unique=True)
    score = IntegerField(default=0)
    last_played = DateTimeField(default=datetime.now)

    class Meta:
        database: Database | None = None
        table_name: str = 'players'


class DatabaseManager:
    """Manages player scores database"""

    def __init__(self, path: str) -> None:
        self._path: str = path
        self._db: None | SqliteDatabase = None

    def add_player(self, name: str, score: int = 0) -> Player:
        """Create a new player"""
        player, created = Player.get_or_create(                            # type: ignore
            name=name,
            defaults={'score': score}
        )

        return player  # type: ignore

    def update_score(self, name: str, score: int) -> Player:
        """Update a player's score"""
        player = Player.get(  # type: ignore
            Player.name == name)
        player.score = score
        player.last_played = datetime.now()
        player.save()  # type: ignore
        return player

    def get_high_scores(self, limit: int = 10) -> List[Player]:
        """Retrieve high scores in descending order"""
        return list(
            Player.select()  # type: ignore
            .order_by(Player.score.desc())  # type: ignore
            .limit(limit)
        )

    def get_player(self, name: str) -> Player:
        """Retrieve a single player by name"""
        return Player.get(Player.name == name)  # type: ignore

    def delete_player(self, name: str) -> bool:
        """Delete a player"""
        result = Player.delete().where(  # type: ignore
            Player.name == name).execute()  # type: ignore
        return result > 0  # type: ignore
    
    def player_exists(self, name: str) -> bool:
        try:
            self.get_player(name)
        except DoesNotExist:
            return False
        return True

    def update_if_better_score(self, name: str, score: int) -> Player:
        player = self.get_player(name)
        if score >= player.score:
            return self.update_score(name, score)
        return player

    def __enter__(self) -> "DatabaseManager":
        self._db = SqliteDatabase(self._path)
        Player._meta.database = self._db
        self._db.create_tables([Player])  # type: ignore
        return self  # type: ignore

    def __exit__(self, exc_type: object, exc_val: object, exc_tb: object) -> None:
        """Context manager exit"""
        if self._db:
            self._db.close()


def create_database_mng() -> DatabaseManager:
    path: str = get_db_path()
    return DatabaseManager(path=path)