from typing import List, Dict
from strategy import ScheduleStrategy

class StudentExamsStrategy(ScheduleStrategy):

    def __init__(self, group_name: str):
        self.group_name = group_name

    def transform(self, data: List[Dict]) -> List[Dict]:
        result = []

        for row in data[1:]:
            if row.get("col_4") != self.group_name:
                continue

            result.append({
                "disciplina": row.get("col_2"),
                "profesor": row.get("col_3"),
                "data": row.get("col_5"),
                "ora": row.get("col_6"),
                "sala": row.get("col_7"),
            })

        return result
