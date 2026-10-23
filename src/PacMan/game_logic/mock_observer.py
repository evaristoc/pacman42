from abc import ABC, abstractmethod
from typing import Any

class IObserver(ABC):
    @abstractmethod
    def notify(self, data: Any) -> None:
        pass


class ObserverTemp(IObserver):
    def notify(self, data: Any) -> None:
        print(f"{data}")
