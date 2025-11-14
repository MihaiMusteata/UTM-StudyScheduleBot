import camelot
import pandas as pd
from factory_method import ScheduleParser, ParserCreator

# ---------------------------
# Concrete Product
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

# ---------------------------
# Concrete Creator
# ---------------------------
class MasterLessonsParserCreator(ParserCreator):
    def factory_method(self) -> ScheduleParser:
        return MasterLessonsScheduleParser()
