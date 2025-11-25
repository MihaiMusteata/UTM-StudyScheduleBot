import json

from patterns.composite.composite import DayComposite, SemesterComposite
from patterns.composite.leaf import ExamLeaf, LessonLeaf


def build_lessons_tree(json_file: str) -> SemesterComposite:
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    semester = SemesterComposite("Semestrul 1 - Lectii")
    days_dict = {}

    for lesson in data[1:]:
        day = lesson.get("col_3", "Necunoscut")
        leaf = LessonLeaf(lesson)
        if day not in days_dict:
            days_dict[day] = DayComposite(day)
        days_dict[day].add(leaf)

    for day_name, day_comp in days_dict.items():
        semester.add(day_comp)

    return semester

def build_exams_tree(json_file: str) -> SemesterComposite:
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    semester = SemesterComposite("Semestrul 1 - Examene")
    days_dict = {}

    for exam in data[1:]:
        date = exam.get("col_5", "Necunoscut")
        leaf = ExamLeaf(exam)
        if date not in days_dict:
            days_dict[date] = DayComposite(date)
        days_dict[date].add(leaf)

    for date_name, day_comp in days_dict.items():
        semester.add(day_comp)

    return semester


if __name__ == "__main__":
    lessons_tree = build_lessons_tree("../factory_method/master-lessons.json")
    exams_tree = build_exams_tree("../factory_method/master-exams.json")

    print("===== ORAR LECȚII =====")
    print(lessons_tree.operation())
    print("\n===== ORAR EXAMENE =====")
    print(exams_tree.operation())