from __future__ import annotations
from abc import ABC, abstractmethod
import json

# ---------------- Observer Pattern ----------------
class Subject(ABC):
    @abstractmethod
    def attach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def notify(self) -> None:
        pass

class Observer(ABC):
    @abstractmethod
    async def update(self, subject: Subject) -> None:
        pass