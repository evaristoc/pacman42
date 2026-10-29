from unittest.mock import Mock

from src.PacMan.game_logic.gamemanager.gamesession import GameSession


def test_session_updates_characters_then_checks_collisions() -> None:
    timer = Mock()
    timer.update.return_value = (False, None)
    timer.level_running = True

    pacman = Mock()
    pacman.position.get_position_from_tile.return_value = (2, 2)
    ghosts = Mock()
    collisions = Mock()
    collisions.update.return_value = (False, None)

    session = GameSession(
        maze=Mock(),
        timemng=timer,
        pacman=pacman,
        ghostmng=ghosts,
        collisionmng=collisions,
    )

    result = session.update(delta_ticks=10, pacman_move=(0, -1))

    assert result == (False, None)
    pacman.update.assert_called_once_with(
        delta_ticks=10,
        new_direction=(0, -1),
    )
    ghosts.update.assert_called_once_with(10, (2, 2))
    collisions.update.assert_called_once_with()
