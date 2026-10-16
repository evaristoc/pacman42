from enum import Enum


class GameState(Enum):
    """Enumeration of all possible game states.

    Attributes:
        START: The initial state before the game begins. Player can
            transition to PLAYING to start the game.
        PLAYING: The active gameplay state where the game loop runs,
            Pac-Man moves, ghosts behave, and collisions are processed.
        PAUSE: The paused state where gameplay is suspended but can be
            resumed. Accessible only from PLAYING state.
        GAME_OVER: The terminal state reached when the game ends (win,
            loss, or quit). No further transitions are possible from this
            state.
    """
    START = 1
    PLAYING = 2
    PAUSE = 3
    GAME_OVER = 4


class GameEndReason(Enum):
    """Enumeration of reasons why the game ended.

    Attributes:
        LOST: The player lost (all lives exhausted or caught by a
            ghost).
        WON: The player won (all pellets collected).
        QUIT: The player explicitly quit the game.
    """
    LOST = 1
    WON = 2
    QUIT = 3


class GameStateError(Exception):
    """Raised when an invalid state transition is attempted.

    This exception indicates that a method was called on the
    GameStateMachine while it was in an incompatible state. For example,
    calling play() while already in the PLAYING state is invalid.
    """
    pass


class GameStateMachine:
    """Manages valid game state transitions and prevents invalid
    operations.

    The GameStateMachine enforces a strict state diagram:
    - START → PLAYING (via play())
    - PLAYING ↔ PAUSE (via play()/pause())
    - START/PLAYING/PAUSE → GAME_OVER (via end())
    - GAME_OVER is terminal (no transitions out)

    Attempting invalid transitions raises GameStateError.
    """

    def __init__(self) -> None:
        """Initialize the game state machine in START state.

        The game begins in START, waiting for play() to be called before
        entering PLAYING state.
        """
        self._gamestate: GameState = GameState.START

    def play(self) -> None:
        """Transition to the PLAYING state.

        Valid from START (initial transition to gameplay) or PAUSE
        (resuming a paused game). Raises GameStateError if called from
        PLAYING or GAME_OVER.

        Raises:
            GameStateError: If called while in PLAYING or GAME_OVER
                state.
        """
        match self._gamestate:
            case GameState.START:
                print(
                    "Transitioning gamestate from start to playing."
                )
                self._gamestate = GameState.PLAYING
                return
            case GameState.PLAYING:
                raise GameStateError(
                    "Used play()-method, while "
                    "self.gamestate == GameState.PLAYING"
                )
            case GameState.PAUSE:
                print(
                    "Transitioning gamestate from pause to playing."
                )
                self._gamestate = GameState.PLAYING
                return
            case GameState.GAME_OVER:
                raise GameStateError(
                    "Used play()-method, while "
                    "self.gamestate == GameState.GAME_OVER"
                )
            case _:
                raise GameStateError(
                    f"Used play()-method on {self.__class__.__name__}, "
                    "while self.gamestate didn't match a valid "
                    "GameState"
                )

    def pause(self) -> None:
        """Transition to the PAUSE state.

        Valid only from PLAYING state, allowing the player to suspend
        gameplay temporarily. Raises GameStateError if called from START,
        PAUSE, or GAME_OVER.

        Raises:
            GameStateError: If called while in START, PAUSE, or
                GAME_OVER state.
        """
        match self._gamestate:
            case GameState.START:
                raise GameStateError(
                    "Used pause()-method, while "
                    "self.gamestate == GameState.START"
                )
            case GameState.PLAYING:
                print(
                    "Transitioning gamestate from playing to pause."
                )
                self._gamestate = GameState.PAUSE
                return
            case GameState.PAUSE:
                raise GameStateError(
                    "Used pause()-method, while "
                    "self.gamestate == GameState.PAUSE"
                )
            case GameState.GAME_OVER:
                raise GameStateError(
                    "Used pause()-method, while "
                    "self.gamestate == GameState.GAME_OVER"
                )
            case _:
                raise GameStateError(
                    f"Used pause()-method on {self.__class__.__name__}, "
                    "while self.gamestate didn't match a valid "
                    "GameState"
                )

    def end(self) -> None:
        """Transition to the GAME_OVER state, ending the game.

        Valid from START, PLAYING, or PAUSE states. Once GAME_OVER is
        reached, no further state transitions are possible. Raises
        GameStateError if called from GAME_OVER.

        Raises:
            GameStateError: If called while already in GAME_OVER state.
        """
        match self._gamestate:
            case GameState.START:
                print(
                    "Transitioning gamestate from start to game-over."
                )
                self._gamestate = GameState.GAME_OVER
                return
            case GameState.PLAYING:
                print(
                    "Transitioning gamestate from playing to game-over."
                )
                self._gamestate = GameState.GAME_OVER
                return
            case GameState.PAUSE:
                print(
                    "Transitioning gamestate from pause to game-over."
                )
                self._gamestate = GameState.GAME_OVER
                return
            case GameState.GAME_OVER:
                raise GameStateError(
                    "Used end()-method, while "
                    "self.gamestate == GameState.GAME_OVER"
                )
            case _:
                raise GameStateError(
                    f"Used end()-method on {self.__class__.__name__}, "
                    "while self.gamestate didn't match a valid "
                    "GameState"
                )


class GameEngine:
    """The main game loop orchestrator and entry point.

    GameEngine coordinates the state machine, update cycle, and rendering
    loop. It ties together all game systems (input handling, physics,
    collision detection, rendering) into a single run loop that executes
    until the game ends.
    """

    def __init__(self) -> None:
        """Initialize the GameEngine with a fresh state machine.

        Creates a new GameStateMachine in START state and prepares the
        engine for execution.
        """
        self.gamestatemachine = GameStateMachine()

    def run(self) -> None:
        """Start and execute the main game loop.

        Runs until the game reaches GAME_OVER state. Each iteration
        processes input, updates game logic, handles collisions, and
        renders the frame. Respects the pause state by skipping updates
        when paused.
        """
        pass

    def _update(self) -> None:
        """Internal method to update all game logic for the current frame.

        Called once per frame when the game is in PLAYING state.
        Responsible for:
        - Moving Pac-Man based on player input
        - Updating ghost AI and positions
        - Detecting collisions with pellets, power-ups, walls, and ghosts
        - Managing pellet consumption and score updates
        - Checking win/loss conditions

        Does nothing if the game is in PAUSE state.
        """
        pass


if __name__ == '__main__':
    gamestate = GameStateMachine()
    gamestate.play()
