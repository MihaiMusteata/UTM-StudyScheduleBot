from abc import ABC, abstractmethod
from typing import List, Dict

class ScheduleStrategy(ABC):

    @abstractmethod
    def transform(self, data: List[Dict]) -> List[Dict]:
        pass


class ScheduleContext:
    def __init__(self, strategy: ScheduleStrategy):
        self._strategy = strategy

    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: ScheduleStrategy):
        self._strategy = strategy

    def process(self, json_data: List[Dict]):
        return self._strategy.transform(json_data)

