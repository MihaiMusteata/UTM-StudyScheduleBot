from typing import List, Dict
from strategy import ScheduleStrategy


class TeacherLessonsStrategy(ScheduleStrategy):

    def transform(self, data: List[Dict]) -> Dict[str, List[Dict]]:
        result = {}

        header = data[0]

        group_cols = {k: v for k, v in header.items() if k.startswith("col_") and v not in ["Data", "ora", "Ziua", "", " "]}

        for row in data[1:]:
            ziua = row.get("col_3", "").strip()
            interval = row.get("col_2", "").strip()
            date_range = row.get("col_1", "").strip()

            for col_key, group_name in group_cols.items():
                cell = row.get(col_key, "").strip()
                if not cell:
                    continue

                disciplina, profesor, sala = self._parse_cell(cell)
                if not profesor:
                    continue

                if profesor not in result:
                    result[profesor] = []

                result[profesor].append({
                    "disciplina": disciplina,
                    "grupa": group_name,
                    "zi": ziua,
                    "interval": interval,
                    "sala": sala,
                    "data": date_range
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
