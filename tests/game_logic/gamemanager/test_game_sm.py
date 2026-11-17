from types import SimpleNamespace
from typing import Any, cast
from unittest.mock import Mock, MagicMock

import pytest

from src.PacMan.game_logic.gamemanager.game_sm import (
    HighScoreRegisterState,
    InGameState,
    InstructionsMenuState,
    MainMenuState,
    PauseMenuState,
    GameOverPlayerLost,
    GameOverPlayerWon
)
from src.PacMan.game_logic.ingame.update_outcome import UpdateOutcome
from src.PacMan.validation_contracts.event_enums import (
    HighScoreRegisterEvents,
    InGameEvents,
    InstructionMenuEvents,
    MainMenuEvents,
    PauseMenuEvents,
)


def make_session(
    outcome: UpdateOutcome = UpdateOutcome.GAME_STILL_GOING,
) -> Mock:
    session = Mock()
    session.timemng.start = Mock()
    session.timemng.pause = Mock()
    session.update.return_value = outcome
    return session


def make_context(session: Mock | None = None) -> Any:
    player = SimpleNamespace(level=1, set_name=Mock(), score=300)
    dbm = MagicMock()
    return SimpleNamespace(
        session=session,
        player=player,
        final_level=Mock(return_value=False),
        create_game_session=Mock(),
        state=None,
        dbm=dbm,
        reset_player=Mock()
    )


def test_event_validation_rejects_wrong_state_event_and_bad_payload() -> None:
    state = MainMenuState(make_context())

    with pytest.raises(ValueError, match='not of type "MainMenuEvents"'):
        state.update_logic({InGameEvents.PAUSE: None}, 1)

    with pytest.raises(ValueError, match="is not a dictionary"):
        state.update_logic(
            cast(Any, {MainMenuEvents.START: "invalid"}),
            1,
        )


def test_event_validation_rejects_falsy_non_dict_payload() -> None:
    state = MainMenuState(make_context())

    with pytest.raises(ValueError, match="is not a dictionary"):
        state.update_logic(
            cast(Any, {MainMenuEvents.START: []}),
            1,
        )


def test_pause_has_priority_over_movement() -> None:
    session = make_session()
    state = InGameState(make_context(session))

    result = state.update_logic(
        {
            InGameEvents.PACMAN_NORTH: None,
            InGameEvents.PAUSE: None,
        },
        1,
    )

    assert isinstance(result, PauseMenuState)
    session.update.assert_not_called()
    session.timemng.pause.assert_called_once_with()


def test_direction_priority_is_independent_of_event_insertion_order() -> None:
    session = make_session()
    state = InGameState(make_context(session))

    state.update_logic(
        {
            InGameEvents.PACMAN_SOUTH: None,
            InGameEvents.PACMAN_NORTH: None,
        },
        1,
    )

    session.update.assert_called_once_with(
        pacman_move=(0, -1),
        delta_ticks=1,
    )


@pytest.mark.parametrize(
    ("event", "expected_move"),
    [
        (InGameEvents.PACMAN_NORTH, (0, -1)),
        (InGameEvents.PACMAN_SOUTH, (0, 1)),
        (InGameEvents.PACMAN_EAST, (1, 0)),
        (InGameEvents.PACMAN_WEST, (-1, 0)),
    ],
)
def test_direction_events_map_to_expected_moves(
    event: InGameEvents,
    expected_move: tuple[int, int],
) -> None:
    session = make_session()
    state = InGameState(make_context(session))

    result = state.update_logic({event: None}, 17)

    assert result is None
    session.update.assert_called_once_with(
        pacman_move=expected_move,
        delta_ticks=17,
    )


def test_continue_restarts_timer_and_preserves_session() -> None:
    session = make_session()
    context = make_context(session)
    paused = PauseMenuState(context)

    resumed = paused.update_logic({PauseMenuEvents.CONTINUE: None}, 1)

    assert isinstance(resumed, InGameState)
    assert context.session is session
    session.timemng.pause.assert_called_once_with()
    session.timemng.start.assert_called_once_with()


def test_pause_exit_wins_over_continue_and_discards_run() -> None:
    session = make_session()
    replacement_session = make_session()
    context = make_context(session)
    context.create_game_session.return_value = replacement_session
    paused = PauseMenuState(context)

    registration = paused.update_logic(
        {
            PauseMenuEvents.CONTINUE: None,
            PauseMenuEvents.EXIT: None,
        },
        1,
    )

    assert isinstance(registration, HighScoreRegisterState)
    assert context.session is None

    menu = registration.update_logic({HighScoreRegisterEvents.CANCEL: None}, 2)
    assert isinstance(menu, MainMenuState)
    game = menu.update_logic({MainMenuEvents.START: None}, 3)

    assert isinstance(game, InGameState)
    assert context.session is replacement_session
    context.create_game_session.assert_called_once_with()


def test_level_win_advances_level_and_replaces_session() -> None:
    session = make_session(UpdateOutcome.ALL_PELLETS_EATEN)
    replacement_session = make_session()
    context = make_context(session)
    context.create_game_session.return_value = replacement_session
    state = InGameState(context)

    result = state.update_logic(None, 1)

    assert isinstance(result, InGameState)
    assert context.player.level == 2
    assert context.session is replacement_session
    context.create_game_session.assert_called_once_with()


@pytest.mark.parametrize(
    ("outcome", "is_final_level"),
    [
        (UpdateOutcome.ALL_LIVES_LOST, False),
        (UpdateOutcome.ALL_PELLETS_EATEN, True),
    ],
)
def test_game_end_clears_session_and_requests_high_score(
    outcome: UpdateOutcome,
    is_final_level: bool,
) -> None:
    session = make_session(outcome)
    context = make_context(session)
    context.final_level.return_value = is_final_level
    state = InGameState(context)

    result = state.update_logic(None, 1)

    if outcome == UpdateOutcome.ALL_LIVES_LOST:
        assert isinstance(result, GameOverPlayerLost)
    if outcome == UpdateOutcome.ALL_PELLETS_EATEN:
        assert isinstance(result, GameOverPlayerWon)


def test_menu_to_game_pause_resume_game_over_and_registration() -> None:
    session = make_session()
    context = make_context()
    context.create_game_session.return_value = session
    db = Mock()

    state = MainMenuState(context).update_logic(
        {MainMenuEvents.START: None}, 1
    )
    assert isinstance(state, InGameState)

    state = state.update_logic({InGameEvents.PAUSE: None}, 2)
    assert isinstance(state, PauseMenuState)

    state = state.update_logic({PauseMenuEvents.CONTINUE: None}, 3)
    assert isinstance(state, InGameState)

    session.update.return_value = UpdateOutcome.ALL_LIVES_LOST
    state = state.update_logic(None, 4)
    assert isinstance(state, GameOverPlayerLost)

    import time
    time.sleep(7)

    state = state.update_logic(None, 5)

    context.dbm.__enter__.return_value = db
    db.player_exists.return_value = False

    if state:
        state = state.update_logic(
            {HighScoreRegisterEvents.REGISTER: {"name": "Ada"}},
            6,
        )
    assert isinstance(state, MainMenuState)
    db.add_player.assert_called_once_with("Ada", 300)


def test_high_score_cancel_returns_to_menu_without_setting_name() -> None:
    context = make_context()

    result = HighScoreRegisterState(context).update_logic(
        {HighScoreRegisterEvents.CANCEL: None},
        1,
    )

    assert isinstance(result, MainMenuState)
    context.player.set_name.assert_not_called()


@pytest.mark.parametrize("payload", [None, {}])
def test_register_without_name_returns_to_menu_without_setting_name(
    payload: dict[str, str] | None,
) -> None:
    context = make_context()
    with pytest.raises(RuntimeError):
        HighScoreRegisterState(context).update_logic(
            {HighScoreRegisterEvents.REGISTER: payload},
            1,
        )

    context.player.set_name.assert_not_called()


def test_instructions_return_to_main_menu() -> None:
    state = InstructionsMenuState(make_context())

    result = state.update_logic({InstructionMenuEvents.RETURN: None}, 1)

    assert isinstance(result, MainMenuState)
