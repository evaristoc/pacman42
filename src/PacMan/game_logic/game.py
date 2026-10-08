from enum import Enum


class GameState(Enum):
    START = 1
    PLAYING = 2
    PAUSE = 3
    GAME_OVER = 4


class GameEndReason(Enum):
    LOST = 1
    WON = 2
    QUIT = 3


class GameStateError(Exception):
    pass


class GameStateMachine:
    def __init__(self) -> None:
        self._gamestate: GameState = GameState.START

    def play(self) -> None:
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
                    f"Used play()-method on {self.__class__.__name__}, while "
                    "self.gamestate didn't match a valid GameState"
                )

    def pause(self)


class GameEngine:
    def __init__(self) -> None:
        self.gamestatemachine = GameStateMachine()

    def run(self) -> None:
        pass

    def _update(self) -> None:
        pass


if __name__ == '__main__':
    gamestate = GameStateMachine()
    gamestate.play()

