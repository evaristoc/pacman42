from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class MenuSnapshot:
    name: str
    buttons: Any


class IMenu(ABC):
    @abstractmethod
    def view(self) -> MenuSnapshot:
        pass
