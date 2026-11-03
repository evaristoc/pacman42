from peewee import Database, SqliteDatabase, Model, CharField, IntegerField, DateTimeField
from pathlib import Path
from typing import Callable
from src.PacMan.database.db_path import get_db_path


class DataBaseManager:
    def __init__(self, db_path: Path = get_db_path()):
        self.db = SqliteDatabase(str(db_path))
        