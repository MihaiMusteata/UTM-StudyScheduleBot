from typing import List, Dict
from strategy import ScheduleStrategy

class TeacherExamsStrategy(ScheduleStrategy):

    def __init__(self, teacher_name: str):
        self.teacher_name = teacher_name

    def transform(self, data: List[Dict]) -> List[Dict]:
        result = []

        for row in data[1:]:
            if row.get("col_3") != self.teacher_name:
                continue

            result.append({
                "disciplina": row.get("col_2"),
                "grupa": row.get("col_4"),
                "data": row.get("col_5"),
                "ora": row.get("col_6"),
                "sala": row.get("col_7"),
            })

        return result
