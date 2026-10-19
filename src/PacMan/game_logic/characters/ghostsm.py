from abc import ABC, abstractmethod
from src.PacMan.game_logic.characters.ghosts import Ghost


class IGhostState(ABC):
    def __init__(self, context: Ghost):
        self.context = context

    @abstractmethod
    def big_pellet_activated(self):
        pass

    @abstractmethod
    def collide_with_pacman(self):
        pass


class ChasingGhostState(IGhostState):
    def big_pellet_activated(self):
        pass


class FrightenedGhostState(IGhostState):
    def big_pellet_activated(self):
        pass


class EatenGhostState(IGhostState):
    def big_pellet_activated(self):
        pass


class ScatterGhostState(IGhostState):
    def big_pellet_activated(self):
        pass
