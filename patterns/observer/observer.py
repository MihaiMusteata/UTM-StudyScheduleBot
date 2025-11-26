from __future__ import annotations
from abc import ABC, abstractmethod

# ---------------- Observer Pattern ----------------
class Subject(ABC):
    @abstractmethod
    def attach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def notify(self, message: str) -> None:
        pass

class Observer(ABC):
    @abstractmethod
    async def update(self, subject: Subject, message: str) -> None:
        pass