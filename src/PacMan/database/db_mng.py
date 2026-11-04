from peewee import SqliteDatabase, Database, Model, CharField, IntegerField, DateTimeField
from src.PacMan.database.db_path import get_db_path
from datetime import datetime
from typing import List


class Player(Model):
    name = CharField(max_length=100, unique=True)
    score = IntegerField(default=0)
    last_played = DateTimeField(default=datetime.now)

    class Meta:
        database: Database | None = None  # Set later
        table_name: str = 'players'


class DatabaseManager:
    """Manages player scores database"""

    def __init__(self, database: SqliteDatabase, Player: type[Player]) -> None:
        self.db: SqliteDatabase = database
        self.Player = Player
        self.db.create_tables([self.Player], safe=True)  # type: ignore

    def add_player(self, name: str, score: int = 0) -> Player:
        """Create a new player"""
        player, created = self.Player.get_or_create(                            # type: ignore
            name=name,
            defaults={'score': score}
        )

        return player  # type: ignore

    def update_score(self, name: str, score: int) -> Player:
        """Update a player's score"""
        player = self.Player.get(  # type: ignore
            self.Player.name == name)
        player.score = score
        player.last_played = datetime.now()
        player.save()  # type: ignore
        return player

    def get_high_scores(self, limit: int = 10) -> List[Player]:
        """Retrieve high scores in descending order"""
        return list(
            self.Player.select()  # type: ignore
            .order_by(self.Player.score.desc())  # type: ignore
            .limit(limit)
        )

    def get_player(self, name: str) -> Player:
        """Retrieve a single player by name"""
        return self.Player.get(self.Player.name == name)  # type: ignore

    def delete_player(self, name: str) -> bool:
        """Delete a player"""
        result = self.Player.delete().where(  # type: ignore
            self.Player.name == name).execute()  # type: ignore
        return result > 0  # type: ignore

    def close(self) -> None:
        """Close database connection"""
        self.db.close()

    def __enter__(self) -> "DatabaseManager":
        """Context manager entry"""
        return self

    def __exit__(self, exc_type: object, exc_val: object, exc_tb: object) -> None:
        """Context manager exit"""
        self.close()

def create_database_mng() -> DatabaseManager:
    path: str = get_db_path()
    db: SqliteDatabase = SqliteDatabase(path)
    if Player._meta.database is not None:
        Player._meta.database.close()  # Clean up old connection
    Player._meta.database = db
    return DatabaseManager(database=db, Player=Player)


if __name__ == '__main__':
    db_manager = create_database_mng()
    with db_manager as db:
        db.delete_player("John")
        scores = db.get_high_scores(10)
        for score in scores:
            print(f"Name: {score.name}, Score: {score.score}")

        # Still have direct access if needed
        advanced_query = db.Player.select().where(db.Player.score > 1000)
