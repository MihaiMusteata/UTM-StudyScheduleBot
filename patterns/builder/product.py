from __future__ import annotations
from typing import Any, Dict


class Notification:
    def __init__(self) -> None:
        self.data: Dict[str, Any] = {}

    def add(self, key: str, value: Any) -> None:
        self.data[key] = value

    def render(self) -> str:
        return (
            f"🔔 Notificare\n"
            f"Tip: {self.data.get('type')}\n"
            f"Persoană: {self.data.get('target')}\n"
            f"Disciplina: {self.data.get('subject')}\n"
            f"Data: {self.data.get('date')}\n"
            f"Ora: {self.data.get('time')}\n"
            f"Sala: {self.data.get('room')}\n"
        )