from src.PacMan.game_logic.ingame.time.time_sm import ITimeState, CountDownState
from dataclasses import dataclass

class TimeError(Exception):
    pass

@dataclass(frozen=True)
class TimeMngSnapshot:
    time_state: str
    countdown_time: int | None
    level_time: int | None

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
        self.state: ITimeState = CountDownState(self)

    def update(self) -> tuple[bool, bool | None]:
        return self.state.update()

    def view(self) -> TimeMngSnapshot:
        return TimeMngSnapshot(time_state=self.state.__class__.__name__,
                               countdown_time=self._discrete_cd_time,
                               level_time=self._discrete_level_time)

    def pause(self) -> None:
        self.state.pause()

    def start(self) -> None:
        self.state.start()

    def restart_countdown(self) -> None:
        self.state.restart_countdown()
