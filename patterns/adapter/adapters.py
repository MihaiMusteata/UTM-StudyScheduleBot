from patterns.adapter.adaptee import ExamJSON, LessonJSON
from patterns.adapter.target import ScheduleTarget

class LessonJSONAdapter(ScheduleTarget):
    def __init__(self, lesson_json: LessonJSON):
        self.lesson_json = lesson_json

    def _parse_value(self, value: str):
        parts = value.split()
        if len(parts) < 2:
            return None
        subject = parts[0]
        lesson_type = parts[1]
        i = 2
        professor_parts = []
        while i < len(parts) and parts[i] != "aud":
            professor_parts.append(parts[i])
            i += 1
        professor = " ".join(professor_parts)
        room = ""
        if i < len(parts) and parts[i] == "aud":
            i += 1
            if i < len(parts):
                room = parts[i]
        return {"subject": subject, "lesson_type": lesson_type, "professor": professor, "room": room}

    def get_records(self):
        if not self.lesson_json.data:
            return []
        headers = self.lesson_json.data[0]
        groups = []
        for i in range(4, 13):  # col_4 to col_12
            col = f"col_{i}"
            if col in headers:
                groups.append((col, headers[col]))
        records = []
        for row in self.lesson_json.data[1:]:
            date_range = row.get("col_1", "").strip()
            time = row.get("col_2", "").strip()
            day = row.get("col_3", "").strip()
            for col, group in groups:
                value = row.get(col, "").strip()
                if value:
                    parsed = self._parse_value(value)
                    if parsed:
                        records.append({
                            "type": parsed["lesson_type"],
                            "subject": parsed["subject"],
                            "professor": parsed["professor"],
                            "student_group": group.strip(),
                            "date": f"{date_range} ({day})",
                            "time": time,
                            "room": parsed["room"]
                        })
        return records

class ExamJSONAdapter(ScheduleTarget):
    def __init__(self, exam_json: ExamJSON):
        self.exam_json = exam_json

    def get_records(self):
        records = []
        for row in self.exam_json.data[1:]:
            records.append({
                "type": "exam",
                "subject": row.get("col_2", "").strip(),
                "professor": row.get("col_3", "").strip(),
                "student_group": row.get("col_4", "").strip(),
                "date": row.get("col_5", "").strip(),
                "time": row.get("col_6", "").strip(),
                "room": row.get("col_7", "").strip()
            })
        return records