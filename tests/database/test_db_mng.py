import pytest
from datetime import datetime
from peewee import DoesNotExist
from pathlib import Path
from typing import Generator

from src.PacMan.database.db_mng import DatabaseManager, Player, create_database_mng


@pytest.fixture
def manager(tmp_path: Path) -> Generator[DatabaseManager, None, None]:
    mgr = DatabaseManager(str(tmp_path / "test.db"))
    with mgr:
        yield mgr


def test_add_player_creates_new_player(manager: DatabaseManager) -> None:
    player = manager.add_player("alice", 10)
    assert player.name == "alice"
    assert player.score == 10
    assert Player.select().count() == 1


def test_add_existing_player_returns_existing_without_changing_score(manager: DatabaseManager) -> None:
    manager.add_player("alice", 10)
    player = manager.add_player("alice", 99)
    assert player.score == 10
    assert Player.select().count() == 1


def test_update_score_changes_score_and_timestamp(manager: DatabaseManager) -> None:
    manager.add_player("bob")
    before = datetime.now()
    player = manager.update_score("bob", 42)
    assert player.score == 42
    assert player.last_played >= before
    assert manager.get_player("bob").score == 42


def test_update_score_missing_player_raises(manager: DatabaseManager) -> None:
    with pytest.raises(DoesNotExist):
        manager.update_score("ghost", 1)


def test_high_scores_are_sorted_and_limited(manager: DatabaseManager) -> None:
    for name, score in [("a", 5), ("b", 50), ("c", 20)]:
        manager.add_player(name, score)
    top = manager.get_high_scores(limit=2)
    assert [p.name for p in top] == ["b", "c"]


def test_delete_player_returns_true_then_false(manager: DatabaseManager) -> None:
    manager.add_player("carl")
    assert manager.delete_player("carl") is True
    assert manager.delete_player("carl") is False


def test_get_player_missing_raises(manager: DatabaseManager) -> None:
    with pytest.raises(DoesNotExist):
        manager.get_player("nobody")

def test_player_exists_returns_right_bool(manager: DatabaseManager) -> None:
    manager.add_player('carl')
    result = manager.player_exists('carl')
    assert result == True
    manager.delete_player('carl')
    result = manager.player_exists('carl')
    assert result == False

def test_update_if_better_score_updates_with_better_score(manager: DatabaseManager) -> None:
    name = 'youp'
    manager.add_player(name, 300)
    player = manager.update_if_better_score(name, 30)
    assert player.score == 300
    player = manager.update_if_better_score(name, 400)
    assert player.score == 400



def test_data_persists_across_sessions(tmp_path: Path) -> None:
    path = str(tmp_path / "persist.db")
    with DatabaseManager(path) as mgr:
        mgr.add_player("dan", 7)
    with DatabaseManager(path) as mgr:
        assert mgr.get_player("dan").score == 7


def test_create_database_mng_uses_configured_path(tmp_path: Path,
                                                  monkeypatch: pytest.MonkeyPatch
                                                  ) -> None:
    import src.PacMan.database.db_mng as dbm
    expected = str(tmp_path / "scores.db")
    monkeypatch.setattr(dbm, "get_db_path", lambda: expected)
    mgr = create_database_mng()
    assert isinstance(mgr, DatabaseManager)


