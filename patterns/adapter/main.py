from patterns.adapter.adaptee import ExamJSON, LessonJSON
from patterns.adapter.adapters import ExamJSONAdapter, LessonJSONAdapter

if __name__ == "__main__":
    lesson_json = LessonJSON("master-lessons.json")
    lesson_adapter = LessonJSONAdapter(lesson_json)
    lesson_records = lesson_adapter.get_records()
    print("Lessons (adapted):")
    print(lesson_records[:3])

    exam_json = ExamJSON("master-exams.json")
    exam_adapter = ExamJSONAdapter(exam_json)
    exam_records = exam_adapter.get_records()
    print("\nExams (adapted):")
    print(exam_records[:3])