from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from src.PacMan.game_logic.ingame.update_outcome import UpdateOutcome
from src.PacMan.app_config.config import COUNTDOWN_TIME, LEVEL_TIME
import time

if TYPE_CHECKING:
    from src.PacMan.game_logic.ingame.time.time import TimeManager


class TimeStateError(Exception):
    pass


class ITimeState(ABC):
    def __init__(self, context: "TimeManager"):
        self.context: "TimeManager" = context

    @abstractmethod
    def update(self) -> UpdateOutcome:
        pass

    @abstractmethod
    def pause(self) -> None:
        pass

    @abstractmethod
    def start_from_pause(self) -> None:
        pass

    @abstractmethod
    def restart_countdown(self) -> None:
        pass


class CountDownState(ITimeState):
    def __init__(self, context: "TimeManager", restart: bool = False):
        self.context: "TimeManager" = context
        self.restart: bool = restart
        self._initialize_countdown()

    def update(self) -> UpdateOutcome:
        new_time = self._get_new_time()
        if new_time < 0:
            self._transition_to_level_active()
        else:
            self._register_new_cd_time(new_time=new_time)
        return UpdateOutcome.GAME_STILL_GOING

    def _initialize_countdown(self) -> None:
        if not self.context._countdown_end_time:
            self.context._countdown_end_time = time.time() + COUNTDOWN_TIME
        else:
            raise TimeStateError(
                "Tried to set countdown end time with value already set.")
        if not self.context._countdown_time_remaining:
            self.context._countdown_time_remaining = COUNTDOWN_TIME
        else:
            raise TimeStateError(
                "Tried to set countdown time remaining with value already set.")
        if not self.context._discrete_cd_time:
            self.context._discrete_cd_time = COUNTDOWN_TIME
        else:
            raise TimeStateError(
                "Tried to set countdown discrete time with value already set.")

    def _get_new_time(self) -> float:
        if not self.context._countdown_end_time:
            raise TimeStateError("Counting down without an endtime.")
        return self.context._countdown_end_time - time.time()

    def _transition_to_level_active(self) -> None:
        self.context._countdown_end_time = None
        self.context._countdown_time_remaining = None
        self.context._discrete_cd_time = None
        self.context.state = LevelActiveState(self.context, self.restart)

    def _register_new_cd_time(self, new_time: float) -> None:
        self.context._countdown_time_remaining = new_time
        new_time_int = int(new_time)
        if new_time_int != self.context._discrete_cd_time:
            self.context._discrete_cd_time = new_time_int

    def pause(self) -> None:
        self.context.state = LevelPauseState(level_active=False,
                                             context=self.context)

    def start_from_pause(self) -> None:
        raise TimeStateError("Tried to start from pause in countdown state")

    def restart_countdown(self) -> None:
        raise TimeStateError(
            "Restarted countdown, while in active countdown state.")


class LevelActiveState(ITimeState):
    def __init__(self, context: "TimeManager", restart: bool = False):
        self.context: "TimeManager" = context
        if not restart:
            self._initialize_timer()
        elif restart and self.context._level_end_time:
            self.context._level_end_time = self.context._level_end_time + time.time()
        else:
            raise TimeStateError("Got restart == True, but no valid end time.")

    def update(self) -> UpdateOutcome:
        new_time = self._get_new_time()
        if new_time < 0:
            return UpdateOutcome.TIME_RAN_OUT
        else:
            self._register_new_cd_time(new_time=new_time)
            return UpdateOutcome.GAME_STILL_GOING

    def _initialize_timer(self) -> None:
        if not self.context._level_end_time:
            self.context._level_end_time = time.time() + LEVEL_TIME
        else:
            raise TimeStateError(
                "Tried to set level end time with value already set.")
        if not self.context._level_time_remaining:
            self.context._level_time_remaining = LEVEL_TIME
        else:
            raise TimeStateError(
                "Tried to set level time remaining with value already set.")
        if not self.context._discrete_cd_time:
            self.context._discrete_level_time = LEVEL_TIME
        else:
            raise TimeStateError(
                "Tried to set level discrete time with value already set.")

    def _get_new_time(self) -> float:
        if not self.context._level_end_time:
            raise TimeStateError(
                "Counting down level time without an endtime.")
        return self.context._level_end_time - time.time()

    def _register_new_cd_time(self, new_time: float) -> None:
        self.context._level_time_remaining = new_time
        new_time_int = int(new_time)
        if new_time_int != self.context._discrete_cd_time:
            self.context._discrete_level_time = new_time_int

    def pause(self) -> None:
        self.context.state = LevelPauseState(level_active=True,
                                             context=self.context)

    def start_from_pause(self) -> None:
        return

    def restart_countdown(self) -> None:
        self.context.state = CountDownState(self.context,
                                            restart=True)


class LevelPauseState(ITimeState):
    def __init__(self, *, level_active: bool, context: "TimeManager"):
        super().__init__(context=context)
        self.level_active = level_active

    def update(self) -> UpdateOutcome:
        return UpdateOutcome.GAME_STILL_GOING

    def pause(self) -> None:
        return

    def start_from_pause(self) -> None:
        if self.level_active:
            time_remaining: float | None = self.context._level_time_remaining
            if not time_remaining:
                raise TimeStateError(
                    "Got level_active == True, but no valid end time.")
            else:
                self.context._level_end_time = (time.time() +
                                                time_remaining)
                self.context.state = LevelActiveState(self.context)
        else:
            time_remaining_cd: float | None = self.context._countdown_time_remaining
            if not time_remaining_cd:
                raise TimeStateError("Got level_active == "
                                     "False, but no valid countdown end time.")
            else:
                self.context._countdown_end_time = (time.time() +
                                                    time_remaining_cd)
                self.context.state = CountDownState(self.context)

    def restart_countdown(self) -> None:
        return
