from patterns.adapter.adaptee import ExamJSON, LessonJSON
from patterns.adapter.target import ScheduleTarget

class LessonJSONAdapter(ScheduleTarget):
    def __init__(self, lesson_json: LessonJSON):
        self.lesson_json = lesson_json

    def get_records(self):
        records = []
        for row in self.lesson_json.data[1:]:
            for col_key, value in row.items():
                if "curs" in value:
                    parts = value.split("\n")
                    subject = parts[0].strip()
                    professor = parts[1].strip() if len(parts) > 1 else ""
                    records.append({
                        "type": "lesson",
                        "subject": subject,
                        "professor": professor,
                        "date": row.get("col_1", "").strip(),
                        "time": row.get("col_2", "").strip(),
                        "room": professor.split()[-1] if professor else ""
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