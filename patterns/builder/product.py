from __future__ import annotations
from typing import Any, Dict


type_map = {
    "sem": "Seminar",
    "lab": "Laborator",
    "curs": "Curs",
    "proiect": "Proiect",
    "exam": "Examen"
}

class Notification:
    def __init__(self) -> None:
        self.data: Dict[str, Any] = {}

    def add(self, key: str, value: Any) -> None:
        self.data[key] = value

    def render(self) -> str:
        target = self.data.get('target')
        target_label = self.data.get('target_label')
        label = f"Profesor: {target_label}" if target == "student" else f"Grupa: {target_label}"

        return (
            f"Data: {self.data.get('date')}\n"
            f"Ora: {self.data.get('time')}\n"
            f"{type_map.get(self.data.get('type'))}: {self.data.get('subject')}\n"
            f"Auditoriu: {self.data.get('room')}\n"
            f"{label}"
        )