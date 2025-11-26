import asyncio

from patterns.observer.observer import Subject, Observer

class LessonsSchedule(Subject):
    def __init__(self, app):
        self.app = app
        self._observers: list[Observer] = []
        self._data = []
        self._is_notifying = False

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    async def notify(self, message: str) -> None:
        if self._is_notifying:
            return
        self._is_notifying = True
        try:
            coros = [observer.update(self, message) for observer in self._observers]
            if coros:
                await asyncio.gather(*coros, return_exceptions=True)
        finally:
            self._is_notifying = False

    def update_schedule(self, message: str):
        asyncio.create_task(self.notify(message))

    @property
    def data(self):
        return self._data


class ExamsSchedule(Subject):
    def __init__(self):
        self._observers: list[Observer] = []
        self._data = []
        self._is_notifying = False

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    async def notify(self, message: str) -> None:
        if self._is_notifying:
            return
        self._is_notifying = True
        try:
            coros = [observer.update(self, message) for observer in self._observers]
            if coros:
                await asyncio.gather(*coros, return_exceptions=True)
        finally:
            self._is_notifying = False

    def update_schedule(self, message: str):
        asyncio.create_task(self.notify(message))

    @property
    def data(self):
        return self._data
