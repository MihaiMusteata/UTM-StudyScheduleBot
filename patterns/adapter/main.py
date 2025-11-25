import json

from patterns.adapter.adaptee import ExamJSON, LessonJSON
from patterns.adapter.adapters import ExamJSONAdapter, LessonJSONAdapter

if __name__ == "__main__":
    lesson_json = LessonJSON("../factory_method/master-lessons.json")
    lesson_adapter = LessonJSONAdapter(lesson_json)
    lesson_records = lesson_adapter.get_records()
    with open("lessons-schedule.json", "w", encoding="utf-8") as f:
        json.dump(lesson_records, f, ensure_ascii=False, indent=2)

    groups = set(record['student_group'] for record in lesson_records)
    with open("groups.json", "w", encoding="utf-8") as f:
        json.dump(list(groups), f, ensure_ascii=False, indent=2)

    professors = set(record['professor'] for record in lesson_records)
    with open("professors.json", "w", encoding="utf-8") as f:
        json.dump(list(professors), f, ensure_ascii=False, indent=2)

    exam_json = ExamJSON("../factory_method/master-exams.json")
    exam_adapter = ExamJSONAdapter(exam_json)
    exam_records = exam_adapter.get_records()
    with open("exams-schedule.json", "w", encoding="utf-8") as f:
        json.dump(exam_records, f, ensure_ascii=False, indent=2)
    print("\nExams (adapted):")
    print(exam_records[:3])