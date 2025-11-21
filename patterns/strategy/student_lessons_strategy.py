from typing import List, Dict
from strategy import ScheduleStrategy

class StudentLessonsStrategy(ScheduleStrategy):

    def __init__(self, group_name: str):
        self.group_name = group_name

    def transform(self, data: List[Dict]) -> List[Dict]:
        result = []

        group_col = None
        header = data[0]

        for key, value in header.items():
            if value.strip() == self.group_name:
                group_col = key
                break

        if group_col is None:
            raise ValueError(f"Grupa {self.group_name} nu există în orar!")

        for row in data[1:]:
            ziua = row.get("col_3", "").strip()
            interval = row.get("col_2", "").strip()
            interval_data = row.get("col_1", "").strip()
            cell = row.get(group_col, "").strip()

            if not ziua or not cell:
                continue

            disciplina, profesor, sala = self._parse_cell(cell)

            result.append({
                "grupa": self.group_name,
                "zi": ziua,
                "interval": interval,
                "disciplina": disciplina,
                "profesor": profesor,
                "sala": sala,
                "data_interval": interval_data
            })

        return result

    def _parse_cell(self, text: str):
        lines = [l.strip() for l in text.split("\n") if l.strip()]

        disciplina = lines[0] if len(lines) > 0 else ""
        profesor = lines[1] if len(lines) > 1 else ""
        sala = ""

        if "aud" in text:
            sala = text.split("aud")[-1].strip()

        return disciplina, profesor, sala
