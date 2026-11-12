from datetime import datetime
from peewee import (SqliteDatabase, Model, CharField, IntegerField,
                    DateTimeField, DatabaseProxy, DoesNotExist)
from src.PacMan.database.db_path import get_db_path

db_proxy = DatabaseProxy()


class Player(Model):
    name: CharField = CharField(max_length=100, unique=True)
    score = IntegerField(default=0)
    last_played = DateTimeField(default=datetime.now)

    class Meta:
        database = db_proxy
        table_name = 'players'


class DatabaseManager:
    def __init__(self, path: str) -> None:
        self._db = SqliteDatabase(path)
        db_proxy.initialize(self._db)

    def __enter__(self) -> "DatabaseManager":
        self._db.connect(reuse_if_open=True)
        self._db.create_tables([Player])  # safe=True is the default
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if not self._db.is_closed():
            self._db.close()

    def add_player(self, name: str, score: int = 0) -> Player:
        """Create a new player"""
        player, created = Player.get_or_create(
            name=name,
            defaults={'score': score}
        )

        return player

    def update_score(self, name: str, score: int) -> Player:
        """Update a player's score"""
        player = Player.get(
            Player.name == name)
        player.score = score
        player.last_played = datetime.now()
        player.save()
        return player

    def get_high_scores(self, limit: int = 10) -> List[Player]:
        """Retrieve high scores in descending order"""
        return list(
            Player.select()
            .order_by(Player.score.desc())
            .limit(limit)
        )

    def get_player(self, name: str) -> Player:
        """Retrieve a single player by name"""
        return Player.get(Player.name == name)

    def delete_player(self, name: str) -> bool:
        """Delete a player"""
        result = Player.delete().where(
            Player.name == name).execute()
        return result > 0

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


def create_database_mng() -> DatabaseManager:
    path: str = get_db_path()
    return DatabaseManager(path=path)
