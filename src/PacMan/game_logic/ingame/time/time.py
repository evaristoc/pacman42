from src.PacMan.game_logic.ingame.time.time_sm import ITimeState, CountDownState
from src.PacMan.game_logic.mock_observer import IObserver
from typing import Any
import time


class TimeError(Exception):
    pass


class TimeManager:
    def __init__(self) -> None:
        self._countdown_end_time: float | None = None
        self._countdown_time_remaining: float | None = None
        self._discrete_cd_time: int | None = None
        self._level_end_time: float | None = None
        self._level_time_remaining: float | None = None
        self._discrete_level_time: int | None = None
        self._counting_down: bool = False
        self.level_running: bool = False
        self._subscribers: list[IObserver] = []
        self.state: ITimeState = CountDownState(self)

    def update(self) -> tuple[bool, bool | None]:
        return self.state.update()

    def pause(self) -> None:
        self.state.pause()

    def start(self) -> None:
        self.state.start()

    def restart_countdown(self) -> None:
        self.state.restart_countdown()

    def subscribe(self, subscriber: IObserver) -> None:
        if subscriber not in self._subscribers:
            self._subscribers.append(subscriber)

    def notify(self, data: dict[str, int]) -> None:
        for subscriber in self._subscribers:
            subscriber.notify(data)
