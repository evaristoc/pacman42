from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
import time

if TYPE_CHECKING:
    from src.PacMan.game_logic.ingame.time.time import TimeManager

COUNTDOWN_TIME = 3
LEVEL_TIME = 300


class TimeStateError(Exception):
    pass


class ITimeState(ABC):
    def __init__(self, context: "TimeManager"):
        self.context: "TimeManager" = context

    @abstractmethod
    def update(self) -> tuple[bool, bool | None]:
        pass

    @abstractmethod
    def pause(self) -> None:
        pass

    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def restart_countdown(self) -> None:
        pass


class CountDownState(ITimeState):
    def __init__(self, context: "TimeManager"):
        self.context: "TimeManager" = context
        self.context.level_running = False

    def update(self) -> tuple[bool, bool | None]:
        game_over = False
        if not self.context._counting_down:
            self.context._countdown_end_time = time.time() + COUNTDOWN_TIME
            self.context._countdown_time_remaining = COUNTDOWN_TIME
            self.context._discrete_cd_time = COUNTDOWN_TIME
            self.context._counting_down = True
            self.context.notify({"Countdown:": self.context._discrete_cd_time})
        else:
            if self.context._countdown_end_time:
                new_time = self.context._countdown_end_time - time.time()
            else:
                raise TimeStateError("Counting down without an endtime.")
            if new_time < 0:
                self.context._countdown_end_time = None
                self.context._countdown_time_remaining = None
                self.context._counting_down = False
                self.context.level_running = True
                self.context.state = LevelActiveState(self.context)
            else:
                self.context._countdown_time_remaining = new_time
                new_time_int = int(new_time)
                if new_time_int != self.context._discrete_cd_time:
                    self.context._discrete_cd_time = new_time_int
                    self.context.notify(
                        {"Countdown:": self.context._discrete_cd_time})
        return (game_over, None)

    def pause(self) -> None:
        self.context.state = LevelPauseState(level_active=False,
                                             context=self.context)

    def start(self) -> None:
        return

    def restart_countdown(self) -> None:
        return RuntimeError("Restarted countdown, while in active countdown state.")


class LevelActiveState(ITimeState):
    def __init__(self, context: "TimeManager"):
        self.context: "TimeManager" = context

    def update(self) -> tuple[bool, bool | None]:
        game_over = False
        if not self.context._level_end_time:
            self.context._level_end_time = time.time() + LEVEL_TIME
            self.context._discrete_level_time = LEVEL_TIME
            self.context.notify(
                {"Time_remaing:": self.context._discrete_level_time})
        new_time = self.context._level_end_time - time.time()
        if new_time < 0:
            self.context.level_running = False
            game_over = True
            level_won = False
            return (game_over, level_won)
        else:
            self.context._level_time_remaining = new_time
            new_time_int = int(new_time)
            if new_time_int != self.context._discrete_level_time:
                self.context._discrete_level_time = new_time_int
                self.context.notify(
                    {"Time_remaing:": self.context._discrete_level_time})
            return (game_over, None)

    def pause(self) -> None:
        self.context.state = LevelPauseState(level_active=True,
                                             context=self.context)

    def start(self) -> None:
        return

    def restart_countdown(self) -> None:
        self.context.state = CountDownState(self.context)


class LevelPauseState(ITimeState):
    def __init__(self, *, level_active: bool, context: "TimeManager"):
        super().__init__(context=context)
        self.level_active = level_active

    def update(self) -> tuple[bool, bool | None]:
        return (False, None)

    def pause(self) -> None:
        return

    def start(self) -> None:
        if self.level_active:
            self.context._level_end_time = time.time() + self.context._level_time_remaining
            self.context.state = LevelActiveState(self.context)
        else:
            self.context._countdown_end_time = time.time() + self.context._countdown_time_remaining
            self.context.state = CountDownState(self.context)

    def restart_countdown(self) -> None:
        return
