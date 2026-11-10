from enum import Enum


class UpdateOutcome(Enum):
    """Enum representing the result of a session update.

    Each outcome is a tuple of (game_over: bool, level_won: bool | None).
    - game_over: True if the game has ended (by any means).
    - level_won: True if the player won the level, False if they lost,
            None if game is still in progress.
    """
    ALL_PELLETS_EATEN = (True, True)
    ALL_LIVES_LOST = (True, False)
    TIME_RAN_OUT = (True, False)
    GAME_STILL_GOING = (False, None)
