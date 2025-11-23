from abc import ABC, abstractmethod


class ScheduleTarget(ABC):
    @abstractmethod
    def get_records(self):
        pass