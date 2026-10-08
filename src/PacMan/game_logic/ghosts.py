from .entities import GameEntity
from .ghostsai import AIStrategy, BlinkyAI, ClydeAI, PinkyAI, InkyAI
from enum import Enum


class GhostState(Enum):
    CHASING = 1
    FRIGHTENED = 2
    EATEN = 3


class GhostName(Enum):
    BLINKY = 1
    PINKY = 2
    INKY = 3
    CLYDE = 4


class GhostError(Exception):
    pass


class GhostStateError(GhostError):
    pass


class Ghost(GameEntity):
    def __init__(self, name: GhostName) -> None:
        self.name: GhostName = name
        self.state: GhostState = GhostState.CHASING
        self.spawn_point: tuple[float, float] = self._get_spawn_point()
        self.strategy: AIStrategy = self._get_ghost_ai()
        self.position: tuple[float, float] = self.spawn_point

    def update(self, delta_time: float) -> None:
        pass

    def render(self) -> None:
        pass

    def get_position(self) -> tuple[float, float]:
        return (0, 0)  # TODO

    def become_frightened(self) -> None:
        pass

    def collide_with_pacman(self) -> None:
        match self.state:
            case GhostState.CHASING:
                return
            case GhostState.FRIGHTENED:
                self.state = GhostState.EATEN
                return
            case GhostState.EATEN:
                return
            case _:
                raise GhostStateError("Somehow self.state inside a Ghost"
                                      "-object was an invalid state.")

    def _get_ghost_ai(self) -> AIStrategy:
        match self.name:
            case GhostName.BLINKY:
                return BlinkyAI(self.spawn_point)
            case GhostName.CLYDE:
                return ClydeAI(self.spawn_point)
            case GhostName.INKY:
                return InkyAI(self.spawn_point)
            case GhostName.PINKY:
                return PinkyAI(self.spawn_point)
            case _:
                raise GhostError("Stored invalid name in Ghost-object, "
                                 "so can't determine valid AIStrategy.")

    def _get_spawn_point(self) -> tuple[float, float]:  # TODO
        match self.name:
            case GhostName.BLINKY:
                return (0, 0)
            case GhostName.CLYDE:
                return (0, 0)
            case GhostName.INKY:
                return (0, 0)
            case GhostName.PINKY:
                return (0, 0)
            case _:
                raise GhostError("Stored invalid name in Ghost-object, "
                                 "so can't determine valid AIStrategy.")
