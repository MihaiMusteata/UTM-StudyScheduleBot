from __future__ import annotations
from abc import ABC, abstractmethod
import camelot
import pandas as pd
from pandas import DataFrame
import json

# ---------------------------
# 1. Product (interfață comună)
# ---------------------------
class ScheduleParser(ABC):
    @abstractmethod
    def parse(self, file_path: str) -> DataFrame:
        pass

# ---------------------------
# 2. Concrete Products
# ---------------------------
class MasterLessonsScheduleParser(ScheduleParser):
    def parse(self, pdf_path: str):
        print(f"[Lesson Parser] Parsing lessons from {pdf_path}")
        tables = camelot.read_pdf(pdf_path, pages='all', flavor='lattice')
        if not tables:
            print("No tables found for lessons.")
            return None
        df = tables[0].df
        df = self._normalize_table(df)
        return df

    def _normalize_table(self, df: pd.DataFrame, target_cols=14):
        if df.shape[1] < target_cols:
            for i in range(df.shape[1], target_cols):
                df[i] = ""
        elif df.shape[1] > target_cols:
            df = df.iloc[:, :target_cols]
        df.columns = [f"col_{i + 1}" for i in range(target_cols)]
        df = df.replace('', pd.NA).dropna(how='all').fillna('')
        return df


class MasterExamScheduleParser(ScheduleParser):
    def parse(self, pdf_path: str):
        print(f"[Exam Parser] Parsing exam from {pdf_path}")
        tables = camelot.read_pdf(pdf_path, pages='all', flavor='lattice')
        if not tables:
            print("No tables found for exams.")
            return None
        df = tables[0].df
        df = self._normalize_table(df)
        return df

    def _normalize_table(self, df: pd.DataFrame, target_cols=7):
        if df.shape[1] < target_cols:
            for i in range(df.shape[1], target_cols):
                df[i] = ""
        elif df.shape[1] > target_cols:
            df = df.iloc[:, :target_cols]
        df.columns = [f"col_{i + 1}" for i in range(target_cols)]
        df = df.replace('', pd.NA).dropna(how='all').fillna('')
        return df


# ---------------------------
# 3. Creator (interfață comună)
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


# ---------------------------
# 4. Concrete Creators
# ---------------------------
class MasterParserCreator(ParserCreator):
    def factory_method(self) -> ScheduleParser:
        return MasterLessonsScheduleParser()


class ExamParserCreator(ParserCreator):
    def factory_method(self) -> ScheduleParser:
        return MasterExamScheduleParser()


# ---------------------------
# 5. Client Code
# ---------------------------
def client_code(creator: ParserCreator, file_path: str, output_json: str):
    df = creator.process_schedule(file_path)
    data = df.to_dict(orient='records')

    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Processed schedule:", data)

if __name__ == "__main__":
    print("📘 Running MASTER parser:")
    client_code(MasterParserCreator(), "../../master-lessons.pdf", "master-lessons.json")

    print("\n📗 Running EXAM parser:")
    client_code(ExamParserCreator(), "../../master-exams.pdf", "master-exams.json")
