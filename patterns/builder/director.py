from __future__ import annotations
from typing import Dict
from patterns.builder.builder import NotificationBuilder


class NotificationDirector:
    def __init__(self):
        self._builder: NotificationBuilder | None = None

    @property
    def builder(self) -> NotificationBuilder:
        return self._builder

    @builder.setter
    def builder(self, builder: NotificationBuilder) -> None:
        self._builder = builder

    def build_student_lesson(self, data: Dict[str, str]) -> None:
        self.builder.set_type("student")
        self.builder.set_target(data["student"])
        self.builder.set_subject_name(data["subject"])
        self.builder.set_date(data["date"])
        self.builder.set_time(data["time"])
        self.builder.set_room(data["room"])

    def build_professor_lesson(self, data: Dict[str, str]) -> None:
        self.builder.set_type("profesor")
        self.builder.set_target(data["professor"])
        self.builder.set_subject_name(data["subject"])
        self.builder.set_date(data["date"])
        self.builder.set_time(data["time"])
        self.builder.set_room(data["room"])

    def build_student_exam(self, data: Dict[str, str]) -> None:
        self.builder.set_type("student")
        self.builder.set_target(data["student"])
        self.builder.set_subject_name(data["subject"])
        self.builder.set_date(data["date"])
        self.builder.set_time(data["time"])
        self.builder.set_room(data["room"])
