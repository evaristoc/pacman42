from typing import Any, cast
from unittest.mock import Mock, call

import pytest

import src.PacMan.game_logic.gamemanager.gamesession as gamesession_module
from src.PacMan.game_logic.gamemanager.gamesession import (
    GameSession,
    GameSessionFactory,
)
from src.PacMan.game_logic.ingame.time.time_sm import (
    CountDownState,
    LevelActiveState,
    LevelPauseState,
)
from src.PacMan.game_logic.ingame.update_outcome import UpdateOutcome


def make_session(
    timer: Mock,
    pacman: Mock | None = None,
    ghosts: Mock | None = None,
    collision: Mock | None = None,
) -> GameSession:
    return GameSession(
        maze=Mock(),
        timemng=timer,
        pacman=pacman or Mock(),
        ghostmng=ghosts or Mock(),
        collisionmng=collision or Mock(),
    )


@pytest.mark.parametrize(
    "outcome",
    [
        UpdateOutcome.ALL_PELLETS_EATEN,
        UpdateOutcome.ALL_LIVES_LOST,
        UpdateOutcome.TIME_RAN_OUT,
    ],
)
def test_terminal_timer_outcome_skips_gameplay_updates(
    outcome: UpdateOutcome,
) -> None:
    timer = Mock()
    timer.update.return_value = outcome
    pacman = Mock()
    ghosts = Mock()
    collision = Mock()
    session = make_session(timer, pacman, ghosts, collision)

    result = session.update(delta_ticks=10)

    assert result is outcome
    pacman.update.assert_not_called()
    ghosts.update.assert_not_called()
    collision.update.assert_not_called()


def test_active_level_updates_characters_and_returns_collision_outcome(
) -> None:
    timer = Mock()
    timer.update.return_value = UpdateOutcome.GAME_STILL_GOING
    timer_context = Mock()
    timer_context._level_end_time = None
    timer_context._level_time_remaining = None
    timer_context._discrete_cd_time = None
    timer.state = LevelActiveState(timer_context)
    pacman = Mock()
    pacman.new_position.get_position_from_tile.return_value = (4, 7)
    pacman.direction = "east"
    ghosts = Mock()
    collision = Mock()
    collision.update.return_value = UpdateOutcome.ALL_LIVES_LOST
    session = make_session(timer, pacman, ghosts, collision)
    update_calls = Mock()
    update_calls.attach_mock(pacman.update, "pacman_update")
    update_calls.attach_mock(ghosts.update, "ghost_update")
    update_calls.attach_mock(collision.update, "collision_update")

    result = session.update(delta_ticks=12, pacman_move=(1, 0))

    assert result is UpdateOutcome.ALL_LIVES_LOST
    pacman.update.assert_called_once_with(
        delta_ticks=12,
        new_direction=(1, 0),
    )
    ghosts.update.assert_called_once_with(12, (4, 7), "east")
    collision.update.assert_called_once_with()
    assert update_calls.mock_calls == [
        call.pacman_update(delta_ticks=12, new_direction=(1, 0)),
        call.ghost_update(12, (4, 7), "east"),
        call.collision_update(),
    ]


def test_countdown_state_skips_gameplay_updates() -> None:
    timer = Mock()
    timer.update.return_value = UpdateOutcome.GAME_STILL_GOING
    timer_context = Mock()
    timer_context._countdown_end_time = None
    timer_context._countdown_time_remaining = None
    timer_context._discrete_cd_time = None
    timer.state = CountDownState(timer_context)
    pacman = Mock()
    ghosts = Mock()
    collision = Mock()
    session = make_session(timer, pacman, ghosts, collision)

    result = session.update(delta_ticks=12)

    assert result is UpdateOutcome.GAME_STILL_GOING
    pacman.update.assert_not_called()
    ghosts.update.assert_not_called()
    collision.update.assert_not_called()


def test_non_active_timer_state_skips_gameplay_updates() -> None:
    timer = Mock()
    timer.update.return_value = UpdateOutcome.GAME_STILL_GOING
    timer.state = LevelPauseState(level_active=True, context=Mock())
    pacman = Mock()
    ghosts = Mock()
    collision = Mock()
    session = make_session(timer, pacman, ghosts, collision)

    result = session.update(delta_ticks=12, pacman_move=(1, 0))

    assert result is UpdateOutcome.GAME_STILL_GOING
    pacman.update.assert_not_called()
    ghosts.update.assert_not_called()
    collision.update.assert_not_called()


def test_view_collects_component_snapshots() -> None:
    timer = Mock()
    timer.view.return_value = "timer snapshot"
    pacman = Mock()
    pacman.view.return_value = "pacman snapshot"
    ghosts = Mock()
    ghosts.view.return_value = "ghost snapshot"
    maze = Mock()
    maze.view.return_value = "maze snapshot"
    session = GameSession(
        maze=maze,
        timemng=timer,
        pacman=pacman,
        ghostmng=ghosts,
        collisionmng=Mock(),
    )

    snapshot = session.view()

    assert snapshot.timemng == "timer snapshot"
    assert snapshot.pacman == "pacman snapshot"
    assert snapshot.ghost_mng == "ghost snapshot"
    assert snapshot.maze == "maze snapshot"
    maze.view.assert_called_once_with()
    timer.view.assert_called_once_with()
    ghosts.view.assert_called_once_with()
    pacman.view.assert_called_once_with()


@pytest.mark.parametrize("level", [0, -1, True, 1.5, "1", None])
def test_factory_rejects_unsupported_levels(level: Any) -> None:
    with pytest.raises(ValueError):
        GameSessionFactory().create_game_new_game(
            cast(Any, level),
            Mock(),
            Mock(),
            False
        )
