from patterns.observer.observer import Subject, Observer
import json

class LessonsSchedule(Subject):
    def __init__(self):
        self._observers: list[Observer] = []
        self._data = []

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        for observer in self._observers:
            import asyncio
            asyncio.create_task(observer.update(self))

    def update_schedule(self, json_file: str):
        with open(json_file, "r", encoding="utf-8") as f:
            self._data = json.load(f)
        self.notify()

    @property
    def data(self):
        return self._data


class ExamsSchedule(Subject):
    def __init__(self):
        self._observers: list[Observer] = []
        self._data = []

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        for observer in self._observers:
            import asyncio
            asyncio.create_task(observer.update(self))

    def update_schedule(self, json_file: str):
        with open(json_file, "r", encoding="utf-8") as f:
            self._data = json.load(f)
        self.notify()

    @property
    def data(self):
        return self._data
