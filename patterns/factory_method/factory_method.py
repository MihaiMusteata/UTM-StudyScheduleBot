from __future__ import annotations
from abc import ABC, abstractmethod
from pandas import DataFrame

# ---------------------------
# Product (interfață comună)
# ---------------------------
class ScheduleParser(ABC):
    @abstractmethod
    def parse(self, file_path: str) -> DataFrame:
        pass

# ---------------------------
# Creator (interfață comună)
# ---------------------------
class ParserCreator(ABC):
    @abstractmethod
    def factory_method(self) -> ScheduleParser:
        pass

    def process_schedule(self, file_path: str) -> DataFrame:
        parser = self.factory_method()
        result = parser.parse(file_path)
        print("✅ Parser finished successfully!")
        return result