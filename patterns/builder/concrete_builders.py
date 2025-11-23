from patterns.builder.builder import NotificationBuilder
from patterns.builder.product import Notification


class LessonNotificationBuilder(NotificationBuilder):
    def __init__(self):
        self.reset()

    def reset(self):
        self._product = Notification()

    @property
    def notification(self) -> Notification:
        product = self._product
        self.reset()
        return product

    def set_type(self, value: str) -> None:
        self._product.add("type", f"Lecție - {value}")

    def set_target(self, value: str) -> None:
        self._product.add("target", value)

    def set_subject_name(self, value: str) -> None:
        self._product.add("subject", value)

    def set_date(self, value: str) -> None:
        self._product.add("date", value)

    def set_time(self, value: str) -> None:
        self._product.add("time", value)

    def set_room(self, value: str) -> None:
        self._product.add("room", value)


class ExamNotificationBuilder(NotificationBuilder):
    def __init__(self):
        self.reset()

    def reset(self):
        self._product = Notification()

    @property
    def notification(self) -> Notification:
        product = self._product
        self.reset()
        return product

    def set_type(self, value: str) -> None:
        self._product.add("type", f"Examen - {value}")

    def set_target(self, value: str) -> None:
        self._product.add("target", value)

    def set_subject_name(self, value: str) -> None:
        self._product.add("subject", value)

    def set_date(self, value: str) -> None:
        self._product.add("date", value)

    def set_time(self, value: str) -> None:
        self._product.add("time", value)

    def set_room(self, value: str) -> None:
        self._product.add("room", value)